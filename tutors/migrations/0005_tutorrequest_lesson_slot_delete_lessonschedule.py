# Generated by Django 4.2.3 on 2023-08-01 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0004_lessonslot_lessonschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorrequest',
            name='lesson_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutors.lessonslot'),
        ),
        migrations.DeleteModel(
            name='LessonSchedule',
        ),
    ]
