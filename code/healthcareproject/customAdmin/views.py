import pymongo
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.db.models import Count
from healthcareapp.models import UserModel
from bson.objectid import ObjectId

# from ..healthcareapp.urls import


# Database configuration
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "healthcareApp"
client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
db = client[MONGODB_DATABASE]


# Create your views here.
def adminDashboard(request):
    user_count = db.healthcareapp_usermodel.count()
    users = UserModel.objects.all()
    print(users)
    print("Dashboard aa gya vhayyyy")
    return render(request , 'dashboard.html' , {'user_count': user_count , 'users': users })

def del_user(request , req_id):
    print(req_id)
    # res = db.healthcareapp_usermodel.delete_one({'id' : req_id})
    res = UserModel.objects.get(id= req_id)
    res.delete()
    # check the deleted record
    print("User deleted")
    return redirect("dashboard")



def logout(request):
    return redirect("LoginPage")