import sweetify
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
import pymongo
from django.http import HttpResponse
from .models import UserModel, passwordToken
from django.core.mail import send_mail
import random
from django.utils import timezone
import string


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
                    sweetify.success(request, "Login successful",
                                   icon="success", timer=5000)
                    return redirect('index')
                else:
                    return HttpResponse("Invalid credentials !! Please try again")
            else:
                return HttpResponse("Authentication failed !! User not found ")


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
            # return render(request,'auth/forgotpwd.html' , msg)
            return HttpResponse("Email does not exists !!")


def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST['otp']
        user = passwordToken.objects.filter(email=email).first()
        email = user.email
        if user.otp == otp:
            print("OTP matched")
            return render(request, 'auth/resetpwd.html', {'email': email})
        else:
            return HttpResponse("Entered OTP is not valid !! try again")


def new_password(request, email):
    if request.method == 'POST':
        password = request.POST['password']
        user = UserModel.objects.filter(email=email).first()
        pwd = make_password(password)
        chnge = UserModel.objects.filter(email=user.email).update(password=pwd)

        if chnge:
            passwordToken.objects.filter(email=email).delete()
            return HttpResponse("Password changed")
        else:
            return HttpResponse("Unable to reset password")


######    USER LOGIN   #####

def index(request):
    if request.session['email_user'] is not None:
        return render(request, "userend/home.html")
    else:
        return redirect("LoginPage")
