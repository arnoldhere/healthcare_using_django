from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('dashboard/' , adminDashboard , name=("dashboard")),
    path("logout/", logout,  name="logout")
]
