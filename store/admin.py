from django.contrib import admin
from .models import Collection, Customer, Product, Promotion

# Register your models here.
admin.site.register(Product)
admin.site.register(Collection)
