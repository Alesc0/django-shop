import sys
import shop.db_handler as DBHandler
from shop.models import Cart_Item
from django.shortcuts import redirect

def addItem(request,product,quantity):
    if(request.user.is_authenticated):
        _,product_= DBHandler.get_product(product)
        cartItem = Cart_Item.objects.get_or_create(user=request.user,product=product_,quantity=quantity)
        if(cartItem[1]):
            cartItem[0].save()
        cookie_cart = None
    else:
        if 'cart' in request.COOKIES:
            cookie_cart = request.COOKIES['cart']
            cart = cookie_cart.split(',')
            cart.append(str(product) + "-" + str(quantity))
            cookie_cart = ",".join(cart)
        else:
            cookie_cart = str(product) + "-" + str(quantity)
    return cookie_cart

def removeItem(request,product):
    if(request.user.is_authenticated):
        cartItem = Cart_Item.objects.get(user=request.user,product=product)
        cartItem.delete()
        cookie_cart = None
    else:
        if 'cart' in request.COOKIES:
            cookie_cart = request.COOKIES['cart']
            cart = cookie_cart.split(',')
            for item in cart:
                item = item.split('-')
                if(item[0] == str(product)):
                    cart.remove(item[0] + "-" + item[1])
            cookie_cart = None if len(cart) == 0 else ",".join(cart)
    return cookie_cart

def editItem(request,product,quantity):
    if(request.user.is_authenticated):
        cartItem = Cart_Item.objects.get(user=request.user,product=product)
        cartItem.quantity = quantity
        cookie_cart = None
        cartItem.save()
    else:
        if 'cart' in request.COOKIES:
            cookie_cart = request.COOKIES['cart']
            cart = cookie_cart.split(',')
            for index,item in enumerate(cart):
                item = item.split('-')
                if(item[0] == str(product)):
                    cart.remove(item[0] + "-" + item[1])
                    cart.insert(index,str(product) + "-" + str(quantity))
            cookie_cart = ",".join(cart)
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

def clearCart(request):
    if(request.user.is_authenticated):
        cartItems = Cart_Item.objects.filter(user=request.user)
        cartItems.delete()
        cookie_cart = None
    else:
        cookie_cart = None
    return cookie_cart