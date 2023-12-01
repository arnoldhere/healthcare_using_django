from django.core.mail import send_mail
import os
import random
from django.contrib.auth.hashers import *
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from healthcareapp.models import *
from django.contrib import messages

# Create your views here.
def staffRegisterPage(request):
    return render(request , 'staffregister.html')

def staffLoginPage(request):
    return render(request , 'stafflogin.html')

def staffLogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # retrive the user from the database
        print(email, password)
        # print(user)
        try:
            staff = StaffModel.objects.get(email=email)
            if staff is not None:
                print("fetched user successfully from the db ", staff)
                fetchpwd = staff.password
                # authenticate the user
                # validate the password
                if staff is not None and check_password(password, fetchpwd):
                    if staff.status == "PENDING" :
                        return redirect('waiting')
                    else:
                        print("user validated in the db")
                        # save the session token of the user
                        fullname = staff.first_name + staff.last_name
                        request.session['staffname'] = fullname
                        request.session['email_user'] = staff.email
                        # Save session data explicitly (usually done automatically)
                        request.session.save()
        
                        messages.success(request, "User logged in successfully")
                        # return redirect("")
                        return HttpResponse("okaie")
                else:
                    messages.error(request , "Authentication failed ! Invalid credentials ")
                    # return HttpResponse("invalid credentials !! try again")
                    return redirect("staffLoginPage")
            elif staff is None:
                messages.error(request, "User not found !!")
                return HttpResponse("User not found !! try again")
        except Exception as e:
                print("User not found !! try again" , e)
                messages.error(request, "User not found !!")
                return redirect("staffLoginPage")
    else:
        return HttpResponse("not a valid request")

def staffRegistration(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        category = request.POST['category']
        resume = request.FILES['resume']
        state =  request.POST['state']
        city =  request.POST['city']
        password = request.POST['password']
        status = "PENDING"

        staff_exists = StaffModel.objects.filter(email=email).first()
        print(staff_exists)

        if staff_exists:
            return HttpResponse("Email is already in use !! try again")

        try:
            if resume.name.endswith(".pdf"):
                imgnameext = email.split('@')
                filenmfinal = resume.name.split('.') 
                filenm =  str(filenmfinal[0]) + '-' + str(imgnameext[0]) + '.pdf'
                # Define the folder where you want to save the image.
                upload_folder = os.path.join(settings.MEDIA_ROOT, 'staff/resumes')
                os.makedirs(upload_folder, exist_ok=True)
                # Construct the file path and save the image.
                file_path = os.path.join(upload_folder, filenm)
                with open(file_path, 'wb+') as destination:
                    for chunk in resume.chunks():
                        destination.write(chunk)
                        
                staff = StaffModel.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    phone=phone,
                    category=category,
                    city=city,
                    state=state,
                    resume=filenm,
                    password=make_password(password),
                    status=status,
                )
                staff.save()
                print("Staff created !!")
                # return redirect('staff') 
                return redirect('waiting')
            else:
                messages.error(request,'Resume must be in pdf format')
                return render(request , 'staffregister.html')
        except Exception as e:
            return HttpResponse(e)

def waitForLoginPage(request):
    return render(request, 'wait.html')


### STAFF CRUD ###

def update_staff(request, req_id):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    phone = request.POST['phone']
    specialization = request.POST['specialization']
    exp = request.POST['exp']
    print(req_id)
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





####### PASSWORD RESET #########

def forgotpwdPage(request):
    return render(request, "forgotpwd.html")

def OTP_generate():
    # token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # return token
    return str(random.randint(100000, 999999))
 
def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)

        user = StaffModel.objects.filter(email=email).first()
        print(user)
        if user:
            otp = OTP_generate()
            user = StaffModel.objects.get(email=email)
            token = passwordToken.objects.create(
                email=user.email,
                otp=otp,
            )
            token.save()
            print(otp)
            # send the otp in email
            subject = "OTP for reset the password"
            message = f"Please verify and check the OTP to reset the password is \n OTP : {otp}"
            from_email = "official.arnold.mac.2004@gmail.com"
            recivers = [user]

            send_mail(subject, message, from_email, recivers)
            # return HttpResponse(f"OTP SENT >>>{otp}")
            return render(request, 'otp.html', {'email': user.email})
        else:
            msg = "Provide valid email address"
            messages.error(request,msg)
            return render(request,'forgotpwd.html' )
            # return HttpResponse("Email does not exists !!")

def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST['otp']
        user = passwordToken.objects.filter(email=email).first()
        email = user.email
        if user.otp == otp:
            print("OTP matched")
            user.delete()
            return render(request, 'resetpwd.html', {'email': email})
        else:
            messages.error(request,"Entered OTP is not valid !!")
            return render(request, 'otp.html', {'email': user.email})

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
    return render(request , 'pwdmsg.html')
