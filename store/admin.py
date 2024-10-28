from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from .models import Collection, Customer, Product, Promotion, Order, OrderItem
from tags.models import TaggedItem


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']  # searching by title
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


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']  # this will add a search bar to search collection
    prepopulated_fields = {
        'slug': ['title']
    }  # this will auto-populate slug field with title
    actions = ['clear_inventory']
    inlines = [TagInline]
    list_display = ['title', 'price', 'inventory_status', 'collection']
    list_editable = ['price']
    list_per_page = 10
    list_filter = ['collection', 'updated_at', InventoryFilter]  # filtering by collection and updated_at
    list_select_related = ['collection']  # this will reduce the number of queries for a foreign key
    search_fields = ['title']  # searching by title

    @admin.display(ordering='inventory')  # sorting by inventory
    def inventory_status(self, product):
        # here we are checking the inventory of product and returning the status
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')  # this will add a button to clear inventory
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} Inventory cleared successfully.', messages.ERROR)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']  # searching by first_name and last_name


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'customer', 'placed_at']
    list_per_page = 10
    list_select_related = ['customer']
