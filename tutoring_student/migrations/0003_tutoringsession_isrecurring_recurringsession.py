# Generated by Django 5.0.3 on 2024-03-16 17:52

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tutoring_student", "0002_alter_student_additionalcomments_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tutoringsession",
            name="isRecurring",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="RecurringSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dayOfWeek", models.CharField(max_length=10)),
                ("time", models.TimeField(verbose_name="Time of Session")),
                ("startDate", models.DateField(verbose_name="Starting Date")),
                ("endDate", models.DateField(verbose_name="Ending Date")),
                (
                    "duration",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=2,
                        validators=[django.core.validators.MaxValueValidator(1.5)],
                        verbose_name="Duration of Session (Hours)",
                    ),
                ),
                ("subject", models.CharField(max_length=100)),
                (
                    "description",
                    models.TextField(
                        verbose_name="Further Description of Student Needs"
                    ),
                ),
                ("gradeLevel", models.CharField(max_length=100)),
                ("preferredPlatform", models.CharField(default="Zoom", max_length=100)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tutoring_student.student",
                    ),
                ),
                (
                    "tutor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tutoring_student.tutor",
                    ),
                ),
            ],
        ),
    ]