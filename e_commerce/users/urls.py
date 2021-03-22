from django.contrib import admin
from django.urls import path 
from .views import register
from .views import login
from .views import getuser
from .views import logout

urlpatterns = [
    
    path('register' , register.as_view()),
    path('login' , login.as_view()),
    path('user' , getuser().as_view()),
     path('logout' , logout().as_view())
]