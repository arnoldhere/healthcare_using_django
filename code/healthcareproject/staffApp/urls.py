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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
