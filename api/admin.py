from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_est', 'parent_category')

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name_est', 'category', 'is_for_sale']
    inlines = [ProductImageInline,]

class SystemParameterAdmin(admin.ModelAdmin):
    list_display = ['key', 'description', 'value']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'status']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SystemParameter, SystemParameterAdmin)
admin.site.register(Order, OrderAdmin)
