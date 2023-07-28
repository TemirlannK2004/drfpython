# Generated by Django 4.2.3 on 2023-07-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutoruser',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='tutorcourses',
            name='course',
        ),
        migrations.AddField(
            model_name='tutorcourses',
            name='course',
            field=models.ManyToManyField(to='tutors.courses'),
        ),
    ]
