from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_est', 'name_rus', 'name_eng', 'parent_category')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    productimage_set = ProductImageSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = (
            'id', 
            'product_code', 
            'name_est', 
            'name_rus', 
            'name_eng', 
            'description_est', 
            'description_rus', 
            'description_eng', 
            'category',
            'quantity',
            'price',
            'image',
            'productimage_set'
            )

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'expires')

class CartProductReadonlySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Product
        fields = (
            'id', 
            'name_est', 
            'name_rus', 
            'name_eng',
            'image'
        )

class CartItemCreateSerializer(serializers.ModelSerializer):   
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

class CartItemUpdateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = CartItem
        fields = ('id', 'quantity')

class CartItemSerializer(serializers.ModelSerializer):   
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'cart')

class OrderUpsertSerializer(serializers.ModelSerializer):   
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone', 'comment', 'shipping_type', 'smartpost_place_id')

class OrderSerializer(serializers.ModelSerializer):   
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    status = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ('id', 'cart', 'full_name', 'email', 'phone', 'comment', 'shipping_type', 'smartpost_place_id', 'status')