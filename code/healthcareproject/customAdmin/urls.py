from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('dashboard/', adminDashboard, name=("dashboard")),
    path("logout/", logout,  name="logout"),
    path("staff/", staffPage, name="staff"),
    path("staffadd/",add_staff , name="addstaff"),
    path("updatestaff/<req_id>", update_staff, name="update_staff"),
    path("delstaff/<req_id>", del_staff, name="del_staff"),
    path("deluser/<req_id>", del_user, name="del_user"),
    path("deltest/<req_id>", del_test, name="del_test"),
    path("updatetest/<req_id>", update_test, name="update_test"),
    path("addtest", add_test, name="add_test"),
    path("test/", testPage, name="test"),
    path("download_excel_staff/",download_staff_data , name="download_staff_data"),
    path("download_excel_lab/",download_labtest_data , name="download_labtest_data"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
