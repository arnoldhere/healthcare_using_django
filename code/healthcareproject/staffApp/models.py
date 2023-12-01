from django.utils import timezone 
from django.db import models

# Create your models here.
class StaffModel(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    # specialization = models.CharField(max_length=25)
    profile_photo = models.ImageField(upload_to="staff/profile/")
    resume = models.CharField(max_length=250,null=True)
    category = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=8,null=True)
    status = models.CharField(max_length=15,null=True)
    city = models.CharField(max_length=25,null=True)
    state = models.CharField(max_length=25,null=True)
    date_joined = models.DateTimeField(default=timezone.now())
    total_visit = models.IntegerField(null=True)