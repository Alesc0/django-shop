from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.logIn, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('admin', views.admin, name='admin'),
    path('addProduct', views.addProduct, name='addProduct'),
    path('addUser', views.addUser, name='addUser'),
    path('cart', views.cart, name='cart'),
    path('addToCart/<id>', views.addToCart, name='addToCart'),
]