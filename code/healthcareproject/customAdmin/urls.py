from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('dashboard/', adminDashboard, name=("dashboard")),
    path("logout/", logout,  name="logout"),

    path("deluser/<req_id>", del_user, name="del_user")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
