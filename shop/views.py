import sys
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import shop.mongo_handler as MongoHandler
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
import shop.forms as forms
import shop.utils

def index(request):
    products = MongoHandler.list_products()
    return render(request, 'index.html',context={'products': products})

def logout(request):
    auth_logout(request)
    return render(request, 'index.html')

def admin(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_superuser:
        return redirect("/")
    users = MongoHandler.list_users()
    products = MongoHandler.list_products()
    return render(request, 'admin.html',context={'users':users, 'products':products})


def logIn(request):
    if request.method == "POST":
        form = forms.loginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if(user is None):
                messages.error(request, "Unsuccessful login. Invalid information.")
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
                messages.error(request, "Unsuccessful registration. Passwords do not match.")
                return render (request, "register.html", context={"form":form})
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.save()
            MongoHandler.create_user(user.id,user.username,form.cleaned_data['email'])
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect ("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = forms.registerForm()
    return render (request, "register.html", context={"form":form})

def addProduct(request):
    if request.method == "POST":
        form = forms.addProductForm(request.POST)
        if form.is_valid():
            MongoHandler.create_product(form.cleaned_data['name'],form.cleaned_data['price'],form.cleaned_data['description'])
            messages.success(request, "Product added successfully." )
            return redirect ("/")
        messages.error(request, "Unsuccessful product addition. Invalid information.")
    form = forms.addProductForm()
    return render (request, "product.html", context={"form":form})

def addUser(request):
    if request.method == "POST":
        form = forms.customUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.save()
            MongoHandler.create_user(user.id,user.username,form.cleaned_data['email'],form.cleaned_data['type'])
            messages.success(request, "User added successfully." )
            return redirect ("/admin")
        messages.error(request, "Unsuccessful user addition. Invalid information.")
    form = forms.customUserForm()
    return render (request, "addUser.html", context={"form":form})

def cart(request,id=None):
    if not request.user.is_authenticated:
        return redirect("/login")
    if id is not None:
        print(id, file=sys.stderr)
        return redirect("/")
    cart = MongoHandler.get_cart(request.user.id)
    return render(request, 'cart.html',context={'cart': cart})

def addToCart(request,id):
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.method == "POST":
        print(request.POST, file=sys.stderr)
    return HttpResponse("success")