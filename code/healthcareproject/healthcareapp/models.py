from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class UserModel(AbstractUser):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=10,unique=True)
#     pincode = models.CharField(max_length=8)
#     state = models.CharField(max_length=20)
#     city = models.CharField(max_length=20)
#     dob = models.DateField(blank=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     userProfile = models.ImageField(upload_to="userProfile")
