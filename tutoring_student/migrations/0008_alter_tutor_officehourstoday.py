# Generated by Django 5.0.3 on 2024-04-03 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tutoring_student", "0007_tutor_officehourstoday"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tutor",
            name="officeHoursToday",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date of Last Office Hours"
            ),
        ),
    ]