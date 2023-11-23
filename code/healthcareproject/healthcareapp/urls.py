from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", Loginpage, name="LoginPage"),
    path("loginpage/", Loginpage, name="LoginPage"),
    path("auth/", Auth, name="auth"),  # login authentication
    path("signup/", SignUp, name="SignUp"),  # sign up authentication
    path("logout/", logout,  name="logout"),

    path("pwdchanged/",show_msg_pwd, name="show_succes"),
    path("reset/", reset_password,  name="reset_password"),
    path("forgotpassword/", forgotpwdPage, name="forgotpassword"),
    path("verify_otp/<str:email>", verify_otp, name="verify_otp"),
    path("newpassword/<str:email>", new_password, name="newpassword"),
    
    path("admin/", adminloginpage, name="adminloginpage"),
    path("adminlogin/",adminlogin, name="adminlogin"),

    path('index/', index, name="index"),
    path("profile/", userProfile, name="userProfile"),
    path("completeprofile/", completeProfile, name="completeProfile"),
    path("editProfile/", editProfile, name="editProfile"),
    
    #### appointment
    path("appointment/", saveappointment, name="bookappointment"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)