# Generated by Django 4.1.10 on 2023-10-17 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcareapp', '0002_appointment_status_alter_usermodel_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='provider',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
