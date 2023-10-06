from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=8)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    dob = models.DateField(blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    userProfile = models.ImageField(upload_to="userProfile")


class StaffModel(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    specialization = models.CharField(max_length=25)
    experience_years = models.PositiveIntegerField()
    date_joined = models.DateTimeField(default=timezone.now)
    profile_photo = models.ImageField(upload_to="staff/profile/")


class LabTestModel(models.Model):
    name = models.CharField(max_length=20)
    cost = models.PositiveIntegerField()
    result_duration = models.PositiveIntegerField()


class passwordToken(models.Model):
    email = models.EmailField(max_length=30)
    otp = models.CharField(max_length=8, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)
