from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32)
    birth_date = models.DateField(null=True)
