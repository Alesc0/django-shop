import sys
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
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

def index(request):
    context = {}
    products = DBHandler.list_products()
    context['products'] = products
    if(request.user.is_authenticated):
        if(request.COOKIES.get('cart') is not None):
            cartUtils.convertCart(request)
            context['cart'] = cartUtils.getCart(request) 
            response = render(request,"index.html",context=context)
            response.delete_cookie('cart')
            return response
    context['cart'] = cartUtils.getCart(request)

    return render(request,"index.html",context=context)

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
    return render(request, 'admin.html',context={'users':users, 'products':products})


def logIn(request):
    if request.method == "POST":
        form = forms.loginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if(user is None):
                form.add_error('password', 'Invalid username or password.')
                return render(request, 'login.html',context={'form':form})
            login(request, user)
            messages.success(request, "Login successful." )
            return redirect ("/")
        messages.error(request, "Unsuccessful login. Invalid information.")
    form = forms.loginForm()
    return render(request, 'login.html',context={'form':form})


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = forms.registerForm(request.POST)
        if form.is_valid():
            if(form.cleaned_data['password1'] != form.cleaned_data['password2']):
                form.add_error('password1', 'Passwords do not match.')
                form.add_error('password2', 'Passwords do not match.')
                return render (request, "register.html", context={"form":form})
            cleanedForm = form.cleaned_data
            try:
                user = DBHandler.create_user(cleanedForm['username'],cleanedForm['password1'],cleanedForm['first_name'],cleanedForm['last_name'], cleanedForm['email'])
            except:
                form.add_error('username', 'Username already exists.')
                return render (request, "register.html", context={"form":form})
            login(request, user)
            return redirect ("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = forms.registerForm()
    return render (request, "register.html", context={"form":form})

def registerComercial(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect("/")
    if request.method == "POST":
        form = forms.comercialUserForm(request.POST)
        if form.is_valid():
            if(form.cleaned_data['password1'] != form.cleaned_data['password2']):
                messages.error(request, "Unsuccessful registration. Passwords do not match.")
                return render (request, "registerComercial.html", context={"form":form})
            cleanedForm = form.cleaned_data
            try:
                user = DBHandler.create_comercial(cleanedForm['username'],cleanedForm['password1'],cleanedForm['first_name'],cleanedForm['last_name'], cleanedForm['email'],cleanedForm['type'],cleanedForm['company'])
            except:
                form.add_error('username', 'Username already exists.')
                return render (request, "registerComercial.html", context={"form":form})
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect ("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = forms.comercialUserForm()
    return render (request, "register.html", context={"form":form})

def addProduct(request):
    if request.method == "POST":
        form = forms.addProductForm(request.POST,request.FILES)
        img = request.FILES['image']
        if form.is_valid():
            fss = FileSystemStorage()
            upload_name = str(uuid.uuid4())
            fss.save(upload_name + ".jpg", img)
            #name, description,price,stock,  image
            DBHandler.create_product(form.cleaned_data['name'],form.cleaned_data['description'],form.cleaned_data['price'],form.cleaned_data['stock'],upload_name)
            return redirect ("/")
        messages.error(request, "Unsuccessful product addition. Invalid information.")
    form = forms.addProductForm()
    return render (request, "product.html", context={"form":form})

def addUser(request):
    if request.method == "POST":
        form = forms.registerForm(request.POST)
        if form.is_valid():
            DBHandler.create_user(form.cleaned_data['username'],form.cleaned_data['password'],form.cleaned_data['first_name'],form.cleaned_data['last_name'], form.cleaned_data['email'],request.user.is_superuser)
            messages.success(request, "Admin added successfully." )
            return redirect ("/admin")
        messages.error(request, "Unsuccessful user addition. Invalid information.")
    form = forms.registerForm()
    return render (request, "addUser.html", context={"form":form})

def cart(request):
    cart = cartUtils.getCart(request)
    return render(request, 'cart.html',context={'cart': cart})

def addToCart(request,id):
    response = HttpResponse()
    if request.method == "GET":
        res = cartUtils.addItem(request,id,1)
        if res != None:
            response.set_cookie('cart',res, max_age=60*60*24*365*2)
        else:
            response.delete_cookie('cart')
        response.content = "success"
    return response

def removeFromCart(request,id):
    response = HttpResponse()
    if request.method == "GET":
        res = cartUtils.removeItem(request,id)
        if res != None:
            response.set_cookie('cart',res, max_age=60*60*24*365*2)
        else:
            response.delete_cookie('cart')
        response.content = "success"
    return response

def changeQuantity(request,id):
    response = HttpResponse()
    if request.method == "GET":
        res = cartUtils.editItem(request,id,request.GET['quantity'])
        if res != None:
            response.set_cookie('cart',res, max_age=60*60*24*365*2)
        else:
            response.delete_cookie('cart')
        response.content = "success"
    return response

