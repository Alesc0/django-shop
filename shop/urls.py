from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.logIn, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('admin', views.admin, name='admin'),
]