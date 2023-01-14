from django.db import models

# Create your models here.

class Cart_Item (models.Model):
    user = models.IntegerField()
    product = models.IntegerField()
    quantity = models.IntegerField()