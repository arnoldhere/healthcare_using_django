from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # render login page
    path("", Loginpage, name="LoginPage"),
    path("loginpage/", Loginpage, name="LoginPage"),
    path("auth/", Auth, name="auth"),  # login authentication
    path("signup/", SignUp, name="SignUp"),  # sign up authentication
    path("logout/", logout,  name="logout"),
    # user screens
    path('index/', index, name="index"),

]
