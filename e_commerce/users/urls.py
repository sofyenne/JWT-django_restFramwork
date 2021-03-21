from django.contrib import admin
from django.urls import path 
from .views import register
from .views import login

urlpatterns = [
    
    path('register' , register.as_view()),
    path('login' , login.as_view())
]