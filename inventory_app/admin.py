from django.contrib import admin
from .models import Category, Supplier, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_info')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'supplier', 'price', 'stock_quantity')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'id')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('id', 'product__name', 'user__username')
