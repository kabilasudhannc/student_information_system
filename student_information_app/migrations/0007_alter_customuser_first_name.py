# Generated by Django 3.2 on 2021-04-11 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_information_app', '0006_auto_20210409_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
