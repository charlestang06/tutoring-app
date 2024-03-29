# Generated by Django 5.0.3 on 2024-03-12 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tutoring_student", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="additionalComments",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="howDidYouHear",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="location",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="onBoardingDate",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date Onboarded"
            ),
        ),
        migrations.AlterField(
            model_name="tutoringsession",
            name="tutor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tutoring_student.tutor",
            ),
        ),
    ]
