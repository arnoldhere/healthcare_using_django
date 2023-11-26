from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("registerform/", staffLoginPage, name="staffLoginPage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
