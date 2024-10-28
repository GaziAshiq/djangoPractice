from django.contrib import admin
from .models import Collection, Customer, Product, Promotion


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory_status']
    list_editable = ['price']
    list_per_page = 10

    @admin.display(ordering='inventory') # sorting by inventory
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


admin.site.register(Collection)
