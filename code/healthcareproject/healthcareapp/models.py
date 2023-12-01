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
    landmark = models.CharField(max_length=25 , null=True)
    house = models.CharField(max_length=35 , null=True)
    dob = models.DateField(blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    userProfile = models.ImageField(upload_to="userProfiles")

class LabTestModel(models.Model):
    name = models.CharField(max_length=20)
    cost = models.PositiveIntegerField()
    result_duration = models.PositiveIntegerField()


class passwordToken(models.Model):
    email = models.EmailField(max_length=30)
    otp = models.CharField(max_length=8, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    aid = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.CharField(max_length=20 , null=True)
    created = timezone.now()
    staff = models.CharField(max_length=50 , null=True)
    user = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=15 , default="PENDING")


class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    user = models.CharField(max_length=25)


class Visit(models.Model):
    vid = models.AutoField(primary_key=True)
    to_staff = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    timestamp=models.DateTimeField(auto_now_add=True)

