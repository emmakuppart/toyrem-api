from django.db import models
from .constants import SystemParameterKey, PaymentType
from django.contrib.postgres.search import SearchVectorExact


models.CharField.register_lookup(SearchVectorExact)


class SystemParameter(models.Model):
    key = models.CharField(max_length=100, primary_key=True, choices=[(tag.value, tag.value) for tag in SystemParameterKey])
    description = models.CharField(max_length=5000, null=True, blank=True)
    value = models.JSONField()

    def __str__(self):
        return self.key


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name_est = models.CharField(max_length=100, unique=True)
    name_rus = models.CharField(max_length=100, unique=True)
    name_eng = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_est


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=255, unique=True)
    name_est = models.CharField(max_length=255)
    name_rus = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255)
    description_est = models.CharField(max_length=5000, null=True, blank=True)
    description_rus = models.CharField(max_length=5000, null=True, blank=True)
    description_eng = models.CharField(max_length=5000, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='images')


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')


class PaymentType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=25, choices=[(tag.value, tag.value) for tag in PaymentType])
    country = models.TextField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to='logos')
    name = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    expires = models.DateTimeField()


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('product', 'cart',)