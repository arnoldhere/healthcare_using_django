from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", Loginpage, name="LoginPage"),
    path("loginpage/", Loginpage, name="LoginPage"),
    path("auth/", Auth, name="auth"),  # login authentication
    path("signup/", SignUp, name="SignUp"),  # sign up authentication
    path("logout/", logout,  name="logout"),
    path("reset/", reset_password,  name="reset_password"),
    path("forgotpassword/", forgotpwdPage, name="forgotpassword"),
    path("verify_otp/<str:email>", verify_otp, name="verify_otp"),
    path("newpassword/<str:email>", new_password, name="newpassword"),
    # user screens
    path('index/', index, name="index"),
    path("admin/", adminloginpage, name="adminloginpage"),
    path("adminlogin/",adminlogin, name="adminlogin"),

]
