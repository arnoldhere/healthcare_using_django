# Generated by Django 4.1.10 on 2023-09-18 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcareapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
