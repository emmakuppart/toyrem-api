import random
import string

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta

from rest_framework import viewsets, generics, pagination, decorators, views, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.decorators import action

from .serializers import *
from .models import *
from .constants import *

CART_SESSION_ID = 'cart'
UNKNOWN_CART_ERROR = 'Unknown cart!'

class IsStaffOrSafe(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'size'
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrSafe,)

def filter_by_name(queryset, lang, name):
    if lang is None or name is None:
        return queryset
    if Language(lang) == Language.et:
        return queryset.filter(name_est__icontains=name)
    if Language(lang) == Language.en:
        return queryset.filter(name_eng__icontains=name)
    if Language(lang) == Language.ru:
        return queryset.filter(name_rus__icontains=name)
    else: return queryset

def filter_by_description(queryset, lang, descr):
    if lang is None or descr is None: 
        return queryset
    elif Language(lang) == Language.et:
        return queryset.filter(description_est__icontains=descr)
    elif Language(lang) == Language.en:
        return queryset.filter(description_eng__icontains=descr)
    elif Language(lang) == Language.ru:
        return queryset.filter(description_rus__icontains=descr)
    else: return queryset

def filter_by_max_price(queryset, max_price):
    if max_price is None: 
        return queryset
    return queryset.filter(price__lte=max_price)

def filter_by_code(queryset, code):
    if code is None:
        return queryset
    return queryset.filter(product_code__icontains=code)

def filter_by_categories(queryset, categories_ids):
    if categories_ids is None or len(categories_ids) == 0:
        return queryset
    return queryset.filter(category__id__in=categories_ids)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsStaffOrSafe,)

    # SELECT * FROM product WHERE to_tsvector(name) @@ to_tsquery(:word)
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(is_for_sale=True)
        lang = self.request.query_params.get('lang')
        queryset = filter_by_categories(queryset, self.request.query_params.get('categoriesIds'))
        queryset = filter_by_code(queryset, self.request.query_params.get('code'))
        queryset = filter_by_name(queryset, lang, self.request.query_params.get('name'))
        queryset = filter_by_description(queryset, lang, self.request.query_params.get('descr'))
        queryset = filter_by_max_price(queryset, self.request.query_params.get('maxPrice'))
        return queryset

def get_session_expiration_time_in_seconds():
    return SystemParameter.objects.get(key=SystemParameterKey.session_expiration_date_in_seconds.value).value['value']

def create_cart(request):
    expires_in = get_session_expiration_time_in_seconds()
    request.data['expires'] = now() + timedelta(seconds=expires_in)
    serializer = CartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    request.session[CART_SESSION_ID] = serializer.data
    request.session.set_expiry(expires_in)
    return serializer.data

def get_cart_id_from_session(request):
    try:
        return request.session[CART_SESSION_ID]['id']
    except KeyError:
        return None

def delete_cart_if_no_items(cart_id):
    items = CartItem.objects.filter(cart=cart_id)
    print(items)

class CartViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ('list'):
            permission_classes = [IsAdminUser,]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def get_active_cart(self, request, pk=None):
        cart_id = get_cart_id_from_session(request)
        if cart_id is None:
            return Response(data=None, status=HTTP_204_NO_CONTENT)
        return Response(CartSerializer(Cart.objects.get(pk=cart_id)).data)


class CartItemViewSet(viewsets.ModelViewSet):
    def list(self, request):
        cart_id = get_cart_id_from_session(request)
        queryset = CartItem.objects.filter(cart=cart_id) 
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['quantity'] < 1:
            return Response(data='Quantity must be at least 1!', status=HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product.objects.all(), pk=request.data['product'])
        if product.is_for_sale is not True:
            return Response(data='Inactive product!', status=HTTP_400_BAD_REQUEST)
            
        if request.data['quantity'] > product.quantity:
            return Response(data='Quantity overload!', status=HTTP_400_BAD_REQUEST)

        cart_id = get_cart_id_from_session(request)
        request.data['cart'] = create_cart(request)['id'] if cart_id is None else cart_id
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['quantity'] < 1:
            return Response(data='Quantity must be at least 1!', status=HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(CartItem.objects.all(), pk=pk)
        product = get_object_or_404(Product.objects.all(), pk=cart_item.product.id)
        if request.data['quantity'] > product.quantity:
            return Response(data='Quantity overload!', status=HTTP_400_BAD_REQUEST)

        cart_id = get_cart_id_from_session(request)
        if cart_id is None or cart_id != cart_item.cart.id:
            return Response(data="Unknown cart!", status=HTTP_400_BAD_REQUEST)

        cart_item.quantity = request.data['quantity']
        cart_item.save(update_fields=["quantity"])
        return Response(CartItemSerializer(cart_item).data)

    def destroy(self, request, pk=None):
        entity = get_object_or_404(CartItem.objects.all(), pk=pk)
        cart_id = get_cart_id_from_session(request)
        if cart_id is None or cart_id != entity.cart.id:
            return Response(data="Inactive cart!", status=HTTP_400_BAD_REQUEST)
        entity.delete()
        return Response(data=None, status=HTTP_204_NO_CONTENT)

def generate_random_string(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_order_number():
    order_number = generate_random_string()
    if Order.objects.filter(order_number=order_number).exists():
        return unique_order_id_generator(instance)
    return order_number

class OrderViewSet(viewsets.ModelViewSet):
    def list(self, request):
        cart_id = get_cart_id_from_session(request)
        queryset = Order.objects.filter(cart=cart_id) 
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cart_id = get_cart_id_from_session(request)
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data if order.cart.id == cart_id else None)

    def create(self, request):
        serializer = OrderUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_id = get_cart_id_from_session(request)
        if cart_id is None:
            return Response(data='No active cart!', status=HTTP_400_BAD_REQUEST) 

        if len(Order.objects.filter(cart=cart_id)) > 0:
            return Response(data='Cart already has an order!', status=HTTP_400_BAD_REQUEST)
    
        request.data['cart'] = cart_id
        request.data['status'] = OrderStatus.received
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = OrderUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_id = get_cart_id_from_session(request)
        order = get_object_or_404(Order.objects.all(), pk=pk)
        if cart_id is None or cart_id != order.cart.id:
            return Response(data='Unknown cart!', status=HTTP_400_BAD_REQUEST)
    
        order.save(update_fields=["full_name", "email", "phone", "comment", "shipping_type", "smartpost_place_id"])
        return Response(OrderSerializer(order).data)

    def destroy(self, request, pk=None):
        return Response(data='Can not delete an order!', status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        cart_id = get_cart_id_from_session(request)
        order = get_object_or_404(Order.objects.all(), pk=pk)

        if cart_id is None or order.cart.id != cart_id:
            return Response(data='Unknown cart!', status=HTTP_400_BAD_REQUEST)

        if order.status != OrderStatus.received.value:
            return Response(data='Already confirmed!', status=HTTP_400_BAD_REQUEST)
        
        order.status = OrderStatus.paid.value
        order.order_number = generate_order_number()
        order.save(update_fields=['order_number', 'status'])
        return Response(OrderSerializer(order).data)