from django.shortcuts import render , redirect
from django.http import HttpResponse
# from ..healthcareapp.urls import

# Create your views here.
def adminDashboard(request):
    print("Dashboard aa gya vhayyyy")
    return render(request , 'dashboard.html')

def logout(request):
    return redirect("LoginPage")