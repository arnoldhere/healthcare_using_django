import pymongo
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.db.models import Count
from healthcareapp.models import UserModel, StaffModel
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
    staff_count = StaffModel.objects.count()
    print(staff_count)
    users = UserModel.objects.all()
    print(users)
    print("Dashboard aa gya vhayyyy")
    return render(request, 'dashboard.html', {'user_count': user_count, 'users': users, 'staff_count': staff_count})


def del_user(request, req_id):
    print(req_id)
    # res = db.healthcareapp_usermodel.delete_one({'id' : req_id})
    res = UserModel.objects.get(id=req_id)
    res.delete()
    # check the deleted record
    print("User deleted")
    return redirect("dashboard")


def staffPage(request):
    staff_count = StaffModel.objects.count()
    staff = StaffModel.objects.all()
    return render(request, 'staff.html', {'staff_count': staff_count , 'staff': staff})


def add_staff(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        specialization = request.POST['specialization']
        exp = request.POST['exp']
        profile = request.POST['profile']

        staff_exists = StaffModel.objects.filter(email=email).first()
        print(staff_exists)

        if staff_exists:
            return HttpResponse("Email is already in use !! try again")

        try:
            staff = StaffModel.objects.create(
                first_name=firstname,
                last_name=lastname,
                email=email,
                phone=phone,
                specialization=specialization,
                experience_years=exp,
                profile_photo=profile
            )
            staff.save()
            print("Staff created !!")
            return redirect('staff')
        except Exception as e:
            return HttpResponse(e)

def del_staff(request, req_id):
    print(req_id)
    # res = db.healthcareapp_usermodel.delete_one({'id' : req_id})
    res = StaffModel.objects.get(id=req_id)
    res.delete()
    # check the deleted record
    print("staff deleted")
    return redirect("staff")

def update_staff(request, req_id):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    phone = request.POST['phone']
    specialization = request.POST['specialization']
    exp = request.POST['exp']

    try:
        data = StaffModel.objects.filter(id=req_id).update(
            first_name=firstname,
            last_name = lastname,
            phone=phone,
            specialization=specialization,
            experience_years=exp
        )
        if data:
            print("updated")
            return redirect("staff")
        else:
            return HttpResponse("Error in updating")

    except Exception as e:
        return HttpResponse(e)


def logout(request):
    return redirect("LoginPage")
