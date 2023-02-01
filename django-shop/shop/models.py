from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Cart_Item (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Sales (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    state = models.CharField(max_length=50)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='auth_user')

class Billing(models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    nif = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Shipping(models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Sales_Item (models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo = models.IntegerField()
    quantity = models.IntegerField()


class Product (models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo = models.IntegerField()
    stock = models.IntegerField()
