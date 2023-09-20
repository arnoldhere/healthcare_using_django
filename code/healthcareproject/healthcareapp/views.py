from django.shortcuts import render, redirect
from pymongo.errors import DuplicateKeyError
from pymongo.collection import ReturnDocument
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
import pymongo
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserModel
# from .forms.register import signUpForm

# Database configuration
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "healthcareApp"
client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
db = client[MONGODB_DATABASE]


###########     Authentication views     ###########
def Loginpage(request):
    return render(request, 'auth/index.html')


def Auth(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # for admin authentication
        if email == "admin@gmail.com" and password == "admin":
            # return HttpResponse("admin logged in")
            print("admin logged in")
            return redirect("dashboard")
        else:
            # retrive the user from the database
            # user = db.users.find_one({'email': email})
            user = UserModel.objects.get(email=email)
            print(user)
            if user is not None:
                # print("fetched user successfully from the db ", user)
                fetchpwd = user.password
                # authenticate the user
                if user is not None and check_password(password, fetchpwd):
                    # print("user validated in the db" + user)
                    # save the session token of the user
                    fullname = user.first_name + user.last_name

                    request.session['Logged_User'] = fullname
                    request.session['email_user'] = user.email
                    # Save session data explicitly (usually done automatically)
                    request.session.save()
                    # return HttpResponse( request.session['Logged_User'])
                    return redirect('index')
                else:
                    return HttpResponse("Authentication failed !! Please enter details carefully ")
            else:
                return HttpResponse("Invalid credentials !! Please try again")


def logout(request):
    request.session.clear()
    # logout(request)
    return redirect('LoginPage')


def SignUp(request):
    if request.method == 'POST':

        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        dob = request.POST['dob']
        phone = request.POST['phone']
        password = request.POST['password']

        print(firstname, lastname, email, phone, password)
        # Check if the email already exists in the User model
        user_exists = UserModel.objects.filter(email=email).first()
        print(user_exists)
        if user_exists:
            return HttpResponse("Email is already used!! try again with the different email")

        try:
            # encrypt the password
            encrypt_password = make_password(password)

            # create a document for usermodel
            user = UserModel.objects.create(
                username = email,
                first_name=firstname,
                last_name=lastname,
                email=email,
                dob=dob,
                phone=phone,
                password=encrypt_password
            )
            # user.save()
            user.save()
            print("user created successfully")
            return redirect('LoginPage')
        except Exception as e:
            print(e)
            # return redirect("LoginPage")
            return HttpResponse("error in storing the user> ", e)
    else:
        return HttpResponse("Error in fetching the form data ")

######    USER LOGIN   #####


def index(request):
    if request.session['email_user'] is not None:
        return render(request, "userend/home.html")
    else:
        return redirect("LoginPage")
