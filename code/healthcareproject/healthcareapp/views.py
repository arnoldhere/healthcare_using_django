from django.conf import settings
import pandas as pd
import xlsxwriter
import os
import tempfile
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
import pymongo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import UserModel, passwordToken , StaffModel  ,Appointment 
from customAdmin.models import Services
from django.core.mail import send_mail
import random
from django.utils import timezone
from django.contrib import messages
from .forms import LoginForm

# Database configuration
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "healthcareApp"
client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
db = client[MONGODB_DATABASE]


########### ADMIN LOGIN   #########
def adminloginpage(request):
    return render(request, 'auth/superuser_login.html')

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'admin@gmail.com' and password == "admin":
            messages.success(request , "Admin login successful")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid credenetials !! try again")
            return redirect("adminloginpage")

###########     Authentication views     ###########
def Loginpage(request):
    if request.session.get('username'):
        return redirect('index')
    return render(request, 'auth/index.html')

def Auth(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # retrive the user from the database
        print(email, password)
        # print(user)
        try:
            user = UserModel.objects.get(email=email)
            if user is not None:
                print("fetched user successfully from the db ", user)
                fetchpwd = user.password
                # authenticate the user
                # validate the password
                if user is not None and check_password(password, fetchpwd):
                    print("user validated in the db")
    
                    # save the session token of the user
                    fullname = user.first_name + user.last_name
                    request.session['username'] = fullname
                    request.session['email_user'] = user.email
                    # Save session data explicitly (usually done automatically)
                    request.session.save()
    
                    messages.success(request, "User logged in successfully")
                    return HttpResponseRedirect(reverse('index'))
                else:
                    messages.error(request , "Authentication failed ! Invalid credentials ")
                    # return HttpResponse("invalid credentials !! try again")
                    return redirect("LoginPage")
            elif user is None:
                messages.error(request, "User not found !!")
                return HttpResponse("User not found !! try again")
        except Exception as e:
                print("User not found !! try again" , e)
                messages.error(request, "User not found !!")
                return redirect("LoginPage")

def logout(request):
    request.session.clear()
    # logout(request)
    return redirect('LoginPage')

def SignUp(request):
    if request.session.get('username'):
        return redirect("index")
    else:
        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email = request.POST['email']
            dob = request.POST['dob']
            phone = request.POST['phone']
            password = request.POST['password']
            # transform the inputs
            str(firstname).title
            str(lastname).title
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
                    username=email,
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

########################  PASSWORD RESET ########################

def forgotpwdPage(request):
    return render(request, "auth/forgotpwd.html")

def OTP_generate():
    # token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # return token
    return str(random.randint(100000, 999999))
 
def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)

        user = UserModel.objects.filter(email=email).first()
        if user:
            otp = OTP_generate()
            user = UserModel.objects.get(email=email)
            token = passwordToken.objects.create(
                email=user.email,
                otp=otp,
            )
            token.save()
            print(otp)
            # send the otp in email
            subject = "OTP for reset the password"
            message = f"Please verify and check the OTP for reset the password is {otp}"
            from_email = "official.arnold.mac.2004@gmail.com"
            recivers = [user]

            send_mail(subject, message, from_email, recivers)
            # return HttpResponse(f"OTP SENT >>>{otp}")
            return render(request, 'auth/otp.html', {'email': user.email})
        else:
            msg = "Provide valid email address"
            messages.error(request,msg)
            return render(request,'auth/forgotpwd.html' )
            # return HttpResponse("Email does not exists !!")

def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST['otp']
        user = passwordToken.objects.filter(email=email).first()
        email = user.email
        if user.otp == otp:
            print("OTP matched")
            user.delete()
            return render(request, 'auth/resetpwd.html', {'email': email})
        else:
            messages.error(request,"Entered OTP is not valid !!")
            return render(request, 'auth/otp.html', {'email': user.email})

def new_password(request, email):
    if request.method == 'POST':
        password = request.POST['password']
        user = UserModel.objects.filter(email=email).first()
        pwd = make_password(password)
        chnge = UserModel.objects.filter(email=user.email).update(password=pwd)

        if chnge:
            passwordToken.objects.filter(email=email).delete()
            print("Password changed")
            return redirect('show_succes')
        else:
            return HttpResponse("Unable to reset password")

def show_msg_pwd(request):
    return render(request , 'auth/pwdmsg.html')

######    USER LOGIN   #####

def index(request):
    if request.session['username'] is not None:
        services = Services.objects.all()
        return render(request, "userend/home.html" , {'services': services})
    else:
        return redirect("LoginPage")

def userProfile(request):
    if request.session['username'] is not None:
        email = request.session['email_user']
        user = UserModel.objects.filter(email=email).first()
        doj = user.date_joined
        img = user.userProfile
        return render(request, 'userend/profile.html' ,{'doj':doj , 'img' : img})
    else:
        return redirect("LoginPage")

def completeProfile(request):
    if request.session['username'] is not None:
        return render(request, "userend/completeProfile.html")
    else:
        return redirect("LoginPage")

def editProfile(request):
    if request.method == "POST":
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phone = request.POST['phone']
            pincode = request.POST['pincode']
            state = request.POST['state']
            city = request.POST['city']
            landmark = request.POST['landmark']
            house = request.POST['house']
            img = request.FILES['photo']


            if img.name.endswith(".jpg"):
                filename = img.name
                # Define the folder where you want to save the image.
                upload_folder = os.path.join(settings.MEDIA_ROOT, 'userProfiles')
                os.makedirs(upload_folder, exist_ok=True)
               # Construct the file path and save the image.
                file_path = os.path.join(upload_folder, filename)
                with open(file_path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)
            else:
                return HttpResponse("Not valid image")           
            # transform the inputs
            str(firstname).title
            str(lastname).title
            # print(firstname, lastname, email, phone)
            try:
                email = request.session['email_user']
                # update a document for usermodel
                user = UserModel.objects.filter(email=email).update(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    phone=phone,
                    pincode = pincode,
                    state = state,
                    city = city,
                    landmark = landmark,
                    house = house,
                    userProfile = img
                )
                # user.save()
                print("user updated successfully")
                return redirect('LoginPage')
            except Exception as e:
                # return redirect("LoginPage")
                return HttpResponse("error in storing >> " , e)
        else:
            return HttpResponse("Error in fetching the form data ")

#### SAVE APPOINTMENT #####
def saveappointment(request):
    if request.method == "POST":
        phone = request.POST['phone']
        service = request.POST['services_list']
        date = request.POST['date']
        time = request.POST['time']
        
        try:
            query  = Appointment.objects.create(
                phone=phone,
                service=service,
                time=time,
                date = date,
                status = "PENDING",
            )
            query.save()
            print("appointment created !!")
            messages.success(request , "Appointment saved - We will contact you soon !!")
            return redirect('index')
        except Exception as e:
            return HttpResponse(e)
