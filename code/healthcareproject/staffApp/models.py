from django.utils import timezone 
from django.db import models

# Create your models here.
class StaffModel(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    specialization = models.CharField(max_length=25)
    experience_years = models.PositiveIntegerField()
    date_joined = models.DateTimeField(default=timezone.now)
    profile_photo = models.ImageField(upload_to="staff/profile/")