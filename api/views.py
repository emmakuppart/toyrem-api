from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta

from rest_framework import viewsets, generics, pagination, decorators, views, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission
from rest_framework.status import HTTP_400_BAD_REQUEST

from .serializers import *
from .models import *
from .constants import SystemParameterKey, Language


CART_SESSION_ID = 'cart'

def cart_view(request, pk):
    if request.method == 'GET':
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return HttpResponse(serializer.data)
    if request.method == 'DELETE':
        queryset = CartItem.objects.all()
        entity = get_object_or_404(queryset, pk=pk)
        entity.delete()
        return HttpResponse(CartSerializer(entity).data)

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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsStaffOrSafe,)

    # SELECT * FROM product WHERE to_tsvector(name) @@ to_tsquery(:word)
    def get_queryset(self):
        queryset = self.queryset
        categoriesIds = self.request.query_params.get('categoriesIds')
        code = self.request.query_params.get('code')
        name = self.request.query_params.get('name')
        lang = self.request.query_params.get('lang')
        if categoriesIds is not None:
            queryset = queryset.filter(category__id__in=categoriesIds)
        if code is not None:
            queryset = queryset.filter(product_code__contains=code)
        if lang is not None and name is not None:
            if Language(lang) == Language.et:
                queryset = queryset.filter(name_est__contains=name)
            if Language(lang) == Language.en:
                queryset = queryset.filter(name_eng__contains=word)
            if Language(lang) == Language.ru:
                queryset = queryset.filter(name_rus__contains=word)
        return queryset


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = (IsStaffOrSafe,)

    def get_queryset(self):
        queryset = self.queryset
        productId = self.request.query_params.get('productId')
        if productId is not None:
            queryset = queryset.filter(product__id=productId)
        return queryset


def get_session_expiration_time_in_seconds():
    return SystemParameter.objects.get(key=SystemParameterKey.session_expiration_date_in_seconds.value).value['value']


class CartViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAdminUser,]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Cart.objects.all()
        entity = get_object_or_404(queryset, pk=pk)
        serializer = CartSerializer(entity)
        return Response(serializer.data)

    def create(self, request):
        try :
            return Response(request.session[CART_SESSION_ID])
        except KeyError:
            expires_in = get_session_expiration_time_in_seconds()
            request.data['expires'] = now() + timedelta(seconds=expires_in)
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            request.session[CART_SESSION_ID] = serializer.data
            request.session.set_expiry(expires_in)
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Cart.objects.all()
        entity = get_object_or_404(queryset, pk=pk)
        serializer = CartSerializer(entity)
        if request.session.is_staff is False and request.session[CART_SESSION_ID]['id'] != serializer['id'].value:
            return Response(data='Unknown cart!', status=HTTP_400_BAD_REQUEST)
        entity.delete()
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAdminUser,]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = CartItem.objects.all()
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            if request.session[CART_SESSION_ID]['cart']['id'] != request.data['cart']:
                return Response(data='Unknown cart!', status=HTTP_400_BAD_REQUEST) 
        except KeyError:
            pass
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = CartItem.objects.all()
        entity = get_object_or_404(queryset, pk=pk)
        serializer = CartItemSerializer(entity)
        if request.session[CART_SESSION_ID]['id'] != serializer['cart'].value:
            return Response(data='Expired cart!', status=HTTP_400_BAD_REQUEST)
        if request.data['quantity'] < 1:
            return Response(data='Quantity must be at least 1!', status=HTTP_400_BAD_REQUEST)
        entity.quantity = request.data['quantity']
        entity.save(update_fields=["quantity"])
        return Response(CartItemSerializer(entity).data)

    def destroy(self, request, pk=None):
        queryset = CartItem.objects.all()
        entity = get_object_or_404(queryset, pk=pk)
        serializer = CartItemSerializer(entity)
        if request.session.is_staff is False and request.session[CART_SESSION_ID]['id'] != serializer['cart'].value:
            return Response(data='Expired cart!', status=HTTP_400_BAD_REQUEST)
        entity.delete()
        return Response(serializer.data)
        