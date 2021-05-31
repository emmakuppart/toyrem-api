from rest_framework import serializers

from .models import Category, Product, Cart, CartItem, ProductImage


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_est', 'name_rus', 'name_eng', 'parent_category')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
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
            'image'
            )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CartInsertSerializer(serializers.ModelSerializer):
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

class CartItemReadonlySerializer(serializers.ModelSerializer):   
    product = CartProductReadonlySerializer(many=False, read_only=True) 
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')


class CartReadonlySerializer(serializers.ModelSerializer):
    cartitem_set = CartItemReadonlySerializer(many=True, required=False)
    class Meta:
        model = Cart
        fields = ('id', 'expires', 'cartitem_set')


class CartItemSerializer(serializers.ModelSerializer):   
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'cart', 'quantity')