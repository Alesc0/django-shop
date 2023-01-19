import sys
from django import template

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