from django.utils import timezone 
from django.db import models

# Create your models here.
class StaffModel(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    specialization = models.CharField(max_length=25)
    profile_photo = models.ImageField(upload_to="staff/profile/")
    resume = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    password = models.CharField(max_length=8)
    date_joined = models.DateTimeField(default=timezone.now)