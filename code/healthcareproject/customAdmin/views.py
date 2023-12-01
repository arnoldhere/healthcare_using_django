import os
from django.core.mail import *
from django.conf import settings
import pymongo
from django.shortcuts import render, redirect
from django.http import HttpResponse , FileResponse
from healthcareapp.models import UserModel, LabTestModel , Appointment
from staffApp.models import *
from .models import Services
import pandas as pd
import xlsxwriter 
from django.contrib import messages
import tempfile
from django.utils import timezone 
from django.utils.dateparse import parse_datetime


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
    print("Dashboard doneee !")
    return render(request, 'dashboard.html', {'user_count': user_count, 'users': users, 'staff_count': staff_count})

def logout(request):
    request.session.clear()
    logout(request)
    return redirect('LoginPage')

def del_user(request, req_id):
    print(req_id)
    # res = db.healthcareapp_usermodel.delete_one({'id' : req_id})
    res = UserModel.objects.get(id=req_id)
    res.delete()
    # check the deleted record
    print("User deleted")
    return redirect("dashboard")

### lab test CRUD ###

def testPage(request):
    tests = LabTestModel.objects.all()
    print(tests)
    tests_count = LabTestModel.objects.count()
    return render(request, 'test.html' , {'tests': tests , 'test_count': tests_count})

def add_test(request):
    if request.method == "POST":
        name = request.POST['name']
        cost = request.POST['cost']
        duration = request.POST['duration']

        test_exists = LabTestModel.objects.filter(name=name).first()
        print(test_exists)

        if test_exists:
            return HttpResponse("test is already published !! try again")

        try:
            test = LabTestModel.objects.create(
                name = name,
                cost = cost,
                result_duration = duration
            )
            test.save()
            print("Test published !!")
            return redirect('test')
        except Exception as e:
            return HttpResponse(e)

def del_test(request, req_id):
    print(req_id)
    # res = db.healthcareapp_usermodel.delete_one({'id' : req_id})
    res = LabTestModel.objects.get(id=req_id)
    res.delete()
    # check the deleted record
    print("Test removed")
    return redirect("test")

def update_test(request, req_id):
    # id = request.POST['id']
    name = request.POST['name']
    cost = request.POST['cost']
    duration = request.POST['duration']
    print(name, cost, duration)
    print(req_id)
    try:
        data = LabTestModel.objects.filter(id=req_id).update(
            name = name,
            cost = cost,
            result_duration = duration
        )
        if data:
            print("updated")
            return redirect("test")
        else:
            return HttpResponse("Error in updating")
    except Exception as e:
        return HttpResponse(e)

### service CRUD ###

def services(request):
    services = Services.objects.all()
    return render(request , 'services.html' , {'services':services })

def add_services(request):
    if request.method == "POST":
        name = request.POST['name']
        type = request.POST['type']
        charge = request.POST['charge']
    
        service_exists = Services.objects.filter(name=name).first()
        print(service_exists)

        if service_exists:
            messages.error(request , "Service already exists")
            return redirect("services")
            # return HttpResponse("Service is already added")

        try:
            Services.objects.create(
                name =name,
                type = type,
                charge = charge
            ) 
            # q.save()
            print("Service added !!")
            return redirect('services')
        except Exception as e:
            print("error >> " , e)
            return HttpResponse(e)

def update_service(request,nm):
    # sid = request.POST['id']
    name = request.POST['name']
    type = request.POST['type']
    charge = request.POST['charge']
    print(id)
    try:
        data = Services.objects.filter(name=nm).update(
            name = name,
            type = type,
            charge = charge
        )
        if data:
            print("updated")
            messages.success(request , "Service updated")
            return redirect("services")
        else:
            messages.error(request , "Service not updated")
            return HttpResponse("Error in updating")
    except Exception as e:
        return HttpResponse(e)

def delete_service(request, nm):
    try:
        # res = db.customAdmin_services.delete_one({'name' : nm})
        res = Services.objects.get(name=nm)
        res.delete()
        if res:
            messages.success(request , "Successfully deleted")
            return redirect("services")
    except Exception as e:
        print("Error in deleting")
        return HttpResponse(e)
    # check the deleted record
    print("removed")
    return redirect("services")

### APPOINTMENT ###

def appointmentPage(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment.html' , {'appointments':appointments})

def appointment_status(request,aid):
    user = request.POST['user']
    a = Appointment.objects.filter(aid=aid).first()
    if a.status == 'PENDING':
        res = Appointment.objects.filter(aid=aid).update(
            status = "CONFIRMED"
        )
        if res:
            subject = "Approved"
            message = f"Your request for home visit has been accepted and our team will reach you soon. "
            from_email ="official.arnold.mac.2004@gmail.com" 
            reciver =[user]
            send_mail(subject, message, from_email, reciver)
            print("mail sent")
            messages.success(request,"Email sent !")
            return redirect('appointmentpage')
    else:
        Appointment.objects.filter(aid=aid).update(
            status = "PENDING"
        ) 
    return redirect('appointmentpage')

def del_appointments(request,aid):
    try:
        # res = db.customAdmin_services.delete_one({'name' : nm})
        res = Appointment.objects.get(aid=aid)
        res.delete()
        if res:
            messages.success(request , "Successfully deleted")
            return redirect("appointmentpage")
    except Exception as e:
        print("Error in deleting")
        return HttpResponse(e)
    # check the deleted record
    print("removed")
    return redirect("appointmentpage")

### STAFF ###
def staffPage(request):
    staff = StaffModel.objects.all()
    return render(request, 'staff.html' , {'staff': staff})

def view_staff(request):
    sid = request.POST['id']
    print(sid)
    staff = StaffModel.objects.filter(id=sid).first()
    print(staff)
    name = staff.first_name + ' ' + staff.last_name
    email = staff.email
    phone = staff.phone
    category = staff.category
    photo = staff.profile_photo
    resume = staff.resume
    location = staff.city + ',' + staff.state
    joined = staff.date_joined
    status = staff.status
    return render(request, 'view_staff.html', {
        'name': name , 'email': email , 'phone': phone , 'category': category , 
        'photo': photo , 'resume' : resume, 'location': location , 'joined': joined , 'status': status   
    })
    
def view_pdf(request,resume):
    file_path = os.path.join('media/staff/resumes' , resume)
    # Ensure the file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf_file:
            response = FileResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{resume}"'
            return response
    else:
        messages.error(request , 'File not found')
        return redirect('staffPage')

def update_staff(request):
    sid = request.POST['id']
    print(sid)
    staff = StaffModel.objects.filter(id=sid).first()
    if staff :
        if staff.status == "PENDING":
            res = StaffModel.objects.filter(id=sid).update(
                status = "CONFIRMED"
            )
            if res:
                messages.success(request , "Staff Activated !")
                return redirect('staffPage')
            else:
                messages.error(request , "Error")
                return redirect('staffPage')    
        elif staff.status == "CONFIRMED":
            res = StaffModel.objects.filter(id=sid).update(
                status = "PENDING"
            )
            if res:
                messages.success(request , "Staff deactivated !")
                return redirect('staffPage')
            else:
                messages.error(request , "Error")
            return redirect('staffPage')    
    else:
        messages.error(request , 'Try again !')
        return redirect('staffPage')
    
    
def del_staff(request, req_id):
    print(req_id)
    res = StaffModel.objects.get(id=req_id)
    res.delete()
    # check the deleted record
    print("staff deleted")
    return redirect("staffPage")


################################################################
#excel file upload & download
#data in excel format
def download_staff_data(request):
    data = StaffModel.objects.all()
    output = tempfile.NamedTemporaryFile(delete=False)
    workbook = xlsxwriter.Workbook(output , {'remove_time': True})
    worksheet = workbook.add_worksheet('staff') 
    row , col = 0 , 0

    #column headers 
    headers = ['First Name', 'Last Name', 'Email', 'Phone', 'Experience' , 'Specialization' , 'date_of_joined']
    for header in headers:
        worksheet.write(row, col, header)
        col+=1
    row+=1
    
    # write the data 
    for i in data:
        worksheet.write(row , 0 , str(i.first_name))
        worksheet.write(row , 1 , str(i.last_name))
        worksheet.write(row , 2 , str(i.email))
        worksheet.write(row , 3 , str(i.phone))
        worksheet.write(row , 4 , str(i.experience_years))
        worksheet.write(row , 5 , str(i.specialization))
        worksheet.write(row , 6 , str(i.date_joined))
        row+=1
    
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read() , content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=staff_data.xlsx'
    print("downloaded successfully")
    return response
    # return redirect('dashboard')

def download_labtest_data(request):
    data = LabTestModel.objects.all()
    output = tempfile.NamedTemporaryFile(delete=False)
    workbook = xlsxwriter.Workbook(output , {'remove_time': True})
    worksheet = workbook.add_worksheet('lab test') 
    row , col = 0 , 0

    #column headers 
    headers = ['NAME', 'COST', 'Result In']
    for header in headers:
        worksheet.write(row, col, header)
        col+=1
    row+=1
    # write the data 
    for i in data:
        worksheet.write(row , 0 , str(i.name))
        worksheet.write(row , 1 , str(i.cost))
        worksheet.write(row , 2 , str(i.result_duration))
        row+=1
    
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read() , content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=labtest_data.xlsx'
    print("downloaded successfully")
    return response
    # return redirect('dashboard')


def download_appointment_data(request):
    data = Appointment.objects.all()
    output = tempfile.NamedTemporaryFile(delete=False)
    workbook = xlsxwriter.Workbook(output , {'remove_time': True})
    worksheet = workbook.add_worksheet('lab test') 
    row , col = 0 , 0
    #column headers 
    headers = ['Phone', 'Service','Date', 'Time' , 'Status']
    for header in headers:
        worksheet.write(row, col, header)
        col+=1
    row+=1
    # write the data 
    for i in data:
        worksheet.write(row , 0 , str(i.phone))
        worksheet.write(row , 1 , str(i.service))
        worksheet.write(row , 2 , str(i.date))
        worksheet.write(row , 3 , str(i.time))
        worksheet.write(row , 4 , str(i.status))
        row+=1
    
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read() , content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=appointment_data.xlsx'
    print("downloaded successfully")
    return response
    # return redirect('dashboard')


def upload_file_staff(request):
    if request.method == 'POST' :
        file = request.FILES['xlsxfile']
        # check the file
        if file.name.endswith('.xlsx') and file is not None:
            #process the file
            df = pd.read_excel(file)
            
            for _ , row in df.iterrows():
              firstname = row['First Name']  
              lastname = row['Last Name']  
              phone = row['Phone']  
              email = row['Email']  
              experience = row['Experience']  
              specialization = row['Specialization']  
            #   doj = row['date_joined']  
            #   if doj.lower() == "nan":
            #         # Handle empty or "nan" values by setting a default datetime
            #         date_joined = timezone.now()  # Default to current datetime
            #   else:
            #         date_joined = parse_datetime(doj)
                #   insert all rows into db
              StaffModel.objects.create(first_name=firstname , last_name = lastname , email = email,phone = phone , experience_years = experience ,specialization = specialization , date_joined = timezone.now())
            
            print("uploaded successfully")
            messages.success(request , "Data Uploaded succesfully !!")
            return redirect('dashboard')
        else:
            messages.error(request , "Can't upload file")
            return redirect('staff')
        
def upload_file_labtest(request):
    if request.method == 'POST' :
        file = request.FILES['xlsxfile']
        # check the file
        if file.name.endswith('.xlsx') and file is not None:
            #process the file
            df = pd.read_excel(file)
            
            for _ , row in df.iterrows():
              name = row['NAME']  
              cost = row['COST']  
              result_duration = row['Result In']  
                #   insert all rows into db
              LabTestModel.objects.create(name=name , cost=cost , result_duration =result_duration  )
            
            print("uploaded successfully")
            messages.success(request , "Data Uploaded succesfully !!")
            return redirect('test')
        else:
            messages.error(request , "Can't upload file")
            return redirect('test')
