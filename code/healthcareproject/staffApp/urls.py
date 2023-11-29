from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("registerform/", staffRegisterPage, name="staffRegisterPage"),
    path("staffregister/", staffRegistration, name="staffRegistration"),
    path("stafflogin/", staffLoginPage, name="staffLoginPage"),
    path("staffAuth/", staffLogin, name="staffLogin"),
    path("wait/", waitForLoginPage, name="waiting"),

    path("pwdchanged/",show_msg_pwd, name="show_succes"),
    path("reset/", reset_password,  name="reset_password"),
    path("forgotpassword/", forgotpwdPage, name="forgotpassword"),
    path("verify_otp/<str:email>", verify_otp, name="verify_otp"),
    path("newpassword/<str:email>", new_password, name="newpassword"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
