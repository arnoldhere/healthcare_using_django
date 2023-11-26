from django.shortcuts import render

# Create your views here.
def staffLoginPage(request):
    return render(request , 'staffregister.html')