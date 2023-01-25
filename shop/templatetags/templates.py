import sys
from django import template
from shop.models import Cart_Item

import shop.mongo_handler as MongoHandler


register = template.Library()

@register.filter(name='private')
def private(obj, attribute):
    return str(obj[attribute])

@register.filter(name='findInCart')
def findInCart(product, cart):
    if cart is None:
        return False
    if type(cart) == list:
        for item in cart:
            item = item.split('-')
            if item[0] == product:
                return True
    else:
        for item in cart:
            if item.product == product:
                return True
        return False

@register.filter(name='limitChars')
def limitChars(string, limit):
    if len(string) > limit:
        return string[:limit] + '...'
    else:
        return string

@register.filter(name='getProduct')
def getProduct(product):
    if isinstance(product,Cart_Item):
        product_ = MongoHandler.get_product(product.product)
        product_["quantity"] = product.quantity
        return product_
    product = product.split('-')
    product_ = MongoHandler.get_product(product[0])
    product_["quantity"] = product[1]
    return product_