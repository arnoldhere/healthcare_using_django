import pymongo
from django.shortcuts import render, redirect
from django.http import HttpResponse
from healthcareapp.models import UserModel, StaffModel , LabTestModel , Appointment
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

### STAFF CRUD ###

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
    sid = request.POST['id']
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

def logout(request):
    request.session.clear()
    logout(request)
    return redirect('LoginPage')

def appointmentPage(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment.html' , {'appointments':appointments})

def appointment_status(request,aid):
    a = Appointment.objects.filter(aid=aid).first()
    if a.status == 'PENDING':
        a.objects.filter(aid=aid).update(
            status = "CONFIRMED"
        )
    else:
        Appointment.objects.filter(aid=aid).update(
            status = "PENDING"
        ) 

    print("done")
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
              firstname = row['FirstName']  
              lastname = row['LastName']  
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
