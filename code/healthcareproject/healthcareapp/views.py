from django.shortcuts import render, redirect
from pymongo.errors import DuplicateKeyError
from pymongo.collection import ReturnDocument
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth import login , logout , authenticate
import pymongo
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Database configuration
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "healthcareApp" 
client = pymongo.MongoClient(host=MONGODB_HOST,port=MONGODB_PORT)
db = client[MONGODB_DATABASE]


###########     Authentication views     ###########    
def Loginpage(request):
    return render(request, 'auth/index.html')

def Auth(request):
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            
            # for admin authentication
            if email == "admin@gmail.com" and password =="admin":
                return HttpResponse("admin logged in")
            else:
                #retrive the user from the database
                # user = db.users.find_one({'email' : email , 'password':password })
                user = db.users.find_one({'email' : email  })
                
                if user is not None :
                    print("fetched user successfully from the db " , user)
                    fetchpwd = user.get('password')
                    #authenticate the user 
                    if user is not None and check_password(password,fetchpwd):
                        print("user validated in the db" , user)
    
                        # save the session token of the user
                        fullname = user['firstname'] + user['lastname']
    
                        request.session['Logged_User'] = fullname 
                        request.session['email_user'] = user['email']
                        # Save session data explicitly (usually done automatically)
                        request.session.save()
                        # return HttpResponse( request.session['Logged_User'])
                        return redirect('index')
                    else:
                        return HttpResponse("Authentication failed")
                else: 
                    return HttpResponse("Invalid credentials !! Please try again") 

def logout(request):
    request.session.clear()
    return redirect('LoginPage')


def SignUp(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        dob = request.POST['dob']
        phone = request.POST['phone']
        password = request.POST['password']

        # Check if the email 
        if db.users.find_one({'email': email}):
            # return render(request , 'auth/index.html')
            return HttpResponse("Email is already taken !! please try again")
        else:
            #encrypt the password
            encrypt_password = make_password(password)
            #create a document 
            users_doc = {
                'firstname' : firstname,
                'lastname' : lastname,
                'email' : email,
                'dob' : dob,
                'phone' : phone ,
                'password' : encrypt_password
            }
    
        try:
            db.users.insert_one(users_doc) # save the document into users collection
            return redirect("LoginPage")
        except DuplicateKeyError:
            return HttpResponse("Error in creating a new user !!" )



######    USER LOGIN   #####
def index(request):
    if request.session['email_user'] is not None:
        return render(request,"userend/home.html")
    else :
        return redirect("LoginPage")