from django.contrib import admin

from .models import Category, Product, SystemParameter, ProductImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_est', 'parent_category')

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name_est', 'category']
    inlines = [ProductImageInline,]

class SystemParameterAdmin(admin.ModelAdmin):
    list_display = ['key', 'description', 'value']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SystemParameter, SystemParameterAdmin)
