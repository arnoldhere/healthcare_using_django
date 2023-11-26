
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('def-admin/', admin.site.urls),
    path("admin/",include('customAdmin.urls')), # connect the urls for customAdmin App
    path('app/', include('healthcareapp.urls')), # include the urls for the app
    path('staff/', include('staffApp.urls')), # include the urls for the app
    path('', include('healthcareapp.urls')), # include the urls for the app
]
