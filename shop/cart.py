import sys
from shop.models import Cart_Item
from django.shortcuts import redirect

def addItem(request,product,quantity):
    if(request.user.is_authenticated):
        cartItem = Cart_Item.objects.get_or_create(user=request.user,product=product,quantity=quantity)
        if(cartItem[1]):
            cartItem[0].save()
        cookie_cart = None
    else:
        if 'cart' in request.COOKIES:
            cookie_cart = request.COOKIES['cart']
            cookie_cart += "," + str(product) + "-" + str(quantity)
        else:
            cookie_cart = str(product) + "-" + str(quantity)
    return cookie_cart

def getCart(request):
    if(request.user.is_authenticated):
        cartItems = Cart_Item.objects.filter(user=request.user)
        return cartItems
    else:
        if 'cart' in request.COOKIES:
            cookie_cart = request.COOKIES['cart']
            cart = cookie_cart.split(',')
            return cart
        else:
            return None

def convertCart(request):
    cookie_cart = request.COOKIES['cart']
    cart = cookie_cart.split(',')
    for item in cart:
        item = item.split('-')
        addItem(request,item[0],item[1])
    return True