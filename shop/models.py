from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cart_Item (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()

class Sales (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
class Sales_Item (models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()