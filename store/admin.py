from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from .models import Collection, Customer, Product, Promotion, Order, OrderItem


# Register your models here.
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')  # sorting by products_count
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({'collection__id': str(collection.id)})
               )  # this will return the url of products with collection id as query parameter in url
        return format_html('<a href="{}">{}</a>', url,
                           collection.products_count)  # this will return the hyperlink of products with collection id

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory_status', 'collection']
    list_editable = ['price']
    list_per_page = 10
    list_select_related = ['collection']  # this will reduce the number of queries for a foreign key

    @admin.display(ordering='inventory')  # sorting by inventory
    def inventory_status(self, product):
        # here we are checking the inventory of product and returning the status
        if product.inventory < 10:
            return 'Low'
        return 'OK'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'placed_at']
    list_per_page = 10
    list_select_related = ['customer']
