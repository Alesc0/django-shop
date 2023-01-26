import sys
from django import template
from shop.models import Cart_Item

import shop.db_handler as DBHandler


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
            if item.product.id == int(product):
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
        id = str(product.product.id)
        quantity = product.quantity
    else:
        split = product.split('-')
        id = split[0]
        quantity = split[1]

    final_prod,_ = DBHandler.get_product(id)
    final_prod["quantity"] = quantity
    return final_prod