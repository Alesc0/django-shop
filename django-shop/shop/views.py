import sys
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import shop.cart as cartUtils
from shop.models import Cart_Item
import shop.db_handler as DBHandler
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
import shop.forms as forms
from django.core.files.storage import FileSystemStorage
import uuid
from django.db import transaction
import datetime
import random


def index(request):
    context = {}
    products = DBHandler.list_products()
    context['products'] = products
    
    date1 = datetime.datetime.now()
    date2 = datetime.datetime.now() - datetime.timedelta(days=1)
    most_bought_today = DBHandler.most_bought_date(date1.date(),date2.date(),5)
    date3 = datetime.datetime.now() - datetime.timedelta(days=30)
    recomendations = DBHandler.most_bought_date(date1.date(),date3.date(),10)
    
    for item in most_bought_today:
        recomendations.remove(item)
    
    while len(recomendations) > 2:
        rand = random.randint(0,len(recomendations)-1)        
        del recomendations[rand]
        
    context['most_bought_today'] = most_bought_today
    context['recomendations'] = recomendations
    if (request.user.is_authenticated):
        if (request.COOKIES.get('cart') is not None):
            cartUtils.convertCart(request)
            context['cart'] = cartUtils.getCart(request)
            response = render(request, "index.html", context=context)
            response.delete_cookie('cart')
            return response
    context['cart'] = cartUtils.getCart(request)

    return render(request, "index.html", context=context)


def logout(request):
    auth_logout(request)
    return redirect("/")


def admin(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_superuser:
        return redirect("/")
    users = DBHandler.list_users()
    products = DBHandler.list_products()
    return render(request, 'admin.html', context={'users': users, 'products': products})


def logIn(request):
    if request.method == "POST":
        form = forms.loginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if (user is None):
                form.add_error('password', 'Invalid username or password.')
                return render(request, 'login.html', context={'form': form})
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful login. Invalid information.")
    form = forms.loginForm()
    return render(request, 'login.html', context={'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = forms.registerForm(request.POST)
        if form.is_valid():
            if (form.cleaned_data['password1'] != form.cleaned_data['password2']):
                form.add_error('password1', 'Passwords do not match.')
                form.add_error('password2', 'Passwords do not match.')
                return render(request, "register.html", context={"form": form})
            cleanedForm = form.cleaned_data
            try:
                user = DBHandler.create_user(cleanedForm['username'], cleanedForm['password1'],
                                             cleanedForm['first_name'], cleanedForm['last_name'], cleanedForm['email'])
            except:
                form.add_error('username', 'Username already exists.')
                return render(request, "register.html", context={"form": form})
            login(request, user)
            return redirect("/")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = forms.registerForm()
    return render(request, "register.html", context={"form": form})


def registerOther(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect("/")
    if request.method == "POST":
        form = forms.comercialUserForm(request.POST)
        print(form.is_valid(),file=sys.stderr)
        if form.is_valid():
            if (form.cleaned_data['password1'] != form.cleaned_data['password2']):
                messages.error(
                    request, "Unsuccessful registration. Passwords do not match.")
                return render(request, "register.html", context={"form": form})
            cleanedForm = form.cleaned_data
            user = DBHandler.create_user(cleanedForm['username'], cleanedForm['password1'], cleanedForm['first_name'],
                                                  cleanedForm['last_name'], cleanedForm['email'], cleanedForm['type'], cleanedForm['company'],is_active = request.user.is_superuser)
            if (user is None):
                form.add_error('username', 'Username already exists.')
                return render(request, "register.html", context={"form": form})
            messages.success(request, "Registration successful.")
            return redirect("admin")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = forms.comercialUserForm()
    return render(request, "register.html", context={"form": form})


def addProduct(request):
    if request.method == "POST":
        form = forms.productForm(request.POST, request.FILES)
        img = request.FILES['image']
        if form.is_valid():
            fss = FileSystemStorage()
            upload_name = str(uuid.uuid4())
            fss.save(upload_name + ".jpg", img)
            DBHandler.create_product(form.cleaned_data['name'], form.cleaned_data['description'],
                                     form.cleaned_data['price'], form.cleaned_data['stock'], upload_name)
            return redirect("/")
        messages.error(
            request, "Unsuccessful product addition. Invalid information.")
    form = forms.productForm()
    return render(request, "product.html", context={"form": form})


def addUser(request):
    if request.method == "POST":
        form = forms.registerForm(request.POST)
        if form.is_valid():
            DBHandler.create_user(form.cleaned_data['username'], form.cleaned_data['password'], form.cleaned_data['first_name'],
                                  form.cleaned_data['last_name'], form.cleaned_data['email'], request.user.is_superuser)
            messages.success(request, "Admin added successfully.")
            return redirect("/admin")
        messages.error(
            request, "Unsuccessful user addition. Invalid information.")
    form = forms.registerForm()
    return render(request, "addUser.html", context={"form": form})


def cart(request):
    cart = cartUtils.getCart(request)
    return render(request, 'cart.html', context={'cart': cart})


def addToCart(request, id):
    response = HttpResponse()
    if request.method == "GET":
        res = cartUtils.addItem(request, id, 1)
        if res != None:
            response.set_cookie('cart', res, max_age=60*60*24*365*2)
        else:
            response.delete_cookie('cart')
        response.content = "success"
    return response


def removeFromCart(request, id):
    response = HttpResponse()
    if request.method == "GET":
        res = cartUtils.removeItem(request, id)
        if res != None:
            response.set_cookie('cart', res, max_age=60*60*24*365*2)
        else:
            response.delete_cookie('cart')
        response.content = "success"
    return response


def changeQuantity(request, id):
    response = HttpResponse()
    if request.method == "GET":
        res = cartUtils.editItem(request, id, request.GET['quantity'])
        if res != None:
            response.set_cookie('cart', res, max_age=60*60*24*365*2)
        else:
            response.delete_cookie('cart')
        response.content = "success"
    return response


@transaction.atomic
def checkoutBilling(request):
    cart = cartUtils.getCart(request)
    if request.method == "POST":
        form = forms.checkoutBillingForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                with transaction.atomic():
                    sale = DBHandler.create_order(
                        request.user.id, cartUtils.getCart(request))
                    DBHandler.link_billing(
                        sale.id, cleaned_data['nif'], cleaned_data['address'],
                        cleaned_data['city'], cleaned_data['zip'], cleaned_data['country'])
            except:
                form.add_error(
                    'nif', 'Error processing order. Please try again.')
                return render(request, "checkoutBilling.html", context={"form": form, "cart": cart})
            
            if cleaned_data['same_for_shipping'] == False:
                return redirect("/checkout/shipping/" + str(sale.id))
            DBHandler.link_shipping(
                sale.id, cleaned_data['address'],
                cleaned_data['city'], cleaned_data['zip'], cleaned_data['country'])
            
            cartUtils.clearCart(request)
            response = redirect("orders")
            response.delete_cookie('cart')
            return response
    form = forms.checkoutBillingForm()
    return render(request, "checkoutBilling.html", context={"form": form, "cart": cart})


def checkoutShipping(request, sale_id):
    if not DBHandler.validate_sale_id(request.user.id, sale_id):
        return redirect("index")
    cart = cartUtils.getCart(request)
    if request.method == "POST":
        form = forms.checkoutShippingForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            DBHandler.link_shipping(sale_id,
                                    cleaned_data['address'],
                                    cleaned_data['city'],
                                    cleaned_data['zip'],
                                    cleaned_data['country'])
            return redirect("orders")
    form = forms.checkoutShippingForm()
    return render(request, "checkoutShipping.html", context={"form": form, "cart": cart})


def orders(request):
    orders = DBHandler.get_orders(request.user.id)
    return render(request, 'orders.html', context={'orders': orders})

def product(request,id):
    context = {}
    product,_ = DBHandler.get_product(id)
    
    date1 = datetime.datetime.now()
    date2 = datetime.datetime.now() - datetime.timedelta(days=1)
    most_bought_today = DBHandler.most_bought_date(date1.date(),date2.date(),5)
    date3 = datetime.datetime.now() - datetime.timedelta(days=30)
    recomendations = DBHandler.most_bought_date(date1.date(),date3.date(),10)
    
    for item in most_bought_today:
        recomendations.remove(item)
    
    while len(recomendations) > 2:
        rand = random.randint(0,len(recomendations)-1)        
        del recomendations[rand]
        
    context['most_bought_today'] = most_bought_today
    context['recomendations'] = recomendations
    
    context['product'] = product
    return render(request, 'product.html', context)

def edit_product(request,id):
    context = {}
    product,_ = DBHandler.get_product(id)
    context['product'] = product
    if request.method == "POST":
        form = forms.editProductForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            DBHandler.edit_product(id, cleaned_data['name'], cleaned_data['description'], cleaned_data['price'], cleaned_data['stock'])
            return redirect("index")
    form = forms.productForm(initial=product)
    return render(request, "product.html", context={"form": form, "product": product})