# Generated by Django 4.1.10 on 2023-10-17 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('charge', models.DecimalField(decimal_places=5, max_digits=10)),
            ],
        ),
    ]
