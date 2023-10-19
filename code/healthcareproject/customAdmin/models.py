from django.db import models

# Create your models here.
class Services(models.Model):
    id = models.AutoField(primary_key=True , null=False)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    charge = models.DecimalField(max_digits=10 , decimal_places=5)