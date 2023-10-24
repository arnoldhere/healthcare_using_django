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
    path("download_appointment/",download_appointment_data , name="download_appointment_data"),
    path("upload_excel_staff/", upload_file_staff, name="upload_file_staff"),
    path("upload_excel_lab/", upload_file_labtest, name="upload_file_labtest"),
    path("services/", services, name="services"),
    path("add_services/", add_services, name="add_services"),
    path("updateservice/<nm>", update_service, name="update_service"),
    path("delete_service/<nm>", delete_service, name="delete_service"),
    path("delete_app/<aid>", del_appointments, name="delete_appointment"),
    path("appointmentpage/", appointmentPage, name="appointmentpage"),
    path("appointmentstatus/<aid>", appointment_status, name="appointment_status"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
