from django.contrib import admin
from product.models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock')
    search_fields = ('title', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
