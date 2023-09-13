from djongo import models 
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Demo(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=3) 
