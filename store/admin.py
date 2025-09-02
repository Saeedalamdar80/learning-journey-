from itertools import product
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    
    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    list_per_page = 10
    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id' : str(collection.id)
               }))
        return format_html('<a href="{}">{}</a>', url, collection.product_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_per_page = 10
    list_editable = ['membership']
    ordering = ['last_name', 'first_name']

    @admin.display(ordering='ordr_count')
    def orders(self, customer):
        url = (reverse('admin:store_order_changelist') 
               + '?'
               + urlencode({
                   'costomer__id' : str(customer.id)
               }))
        return format_html('<a href="{}">{}</a>', url, customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']