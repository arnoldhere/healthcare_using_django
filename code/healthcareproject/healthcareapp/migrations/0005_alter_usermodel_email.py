# Generated by Django 4.1.10 on 2023-10-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcareapp', '0004_alter_usermodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
