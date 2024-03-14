from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
import datetime


class Student(models.Model):
    """
    Model for a student.
    """

    def __str__(self):
        return self.studentName

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentName = models.CharField(max_length=100)
    email = models.EmailField("Email Address")
    password = models.CharField(max_length=100, default="123456")
    phone = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    # Additional Information
    howDidYouHear = models.CharField(max_length=100, null=True, blank=True)
    additionalComments = models.TextField(null=True, blank=True)


class Tutor(models.Model):
    """
    Model for a tutor.
    """

    def __str__(self):
        return self.tutorName

    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutorName = models.CharField(max_length=100)
    email = models.EmailField("Email Address")
    password = models.CharField(max_length=100, default="123456")
    phone = models.CharField(max_length=15, null=True)
    onBoardingDate = models.DateField("Date Onboarded", null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)


class TutoringSession(models.Model):
    """
    Model for a tutoring session.
    """

    def __str__(self):
        return (
            self.student.studentName
            + " - "
            + str(self.date)
            + " - "
            + str(self.time)
            + " - "
            + self.subject
        )

    # Session Information
    date = models.DateField("Date of Session")
    time = models.TimeField("Time of Session")
    duration = models.DecimalField(
        "Duration of Session (Hours)",
        max_digits=2,
        decimal_places=1,
        validators=[MaxValueValidator(1.5)],
    )
    subject = models.CharField(max_length=100)
    description = models.TextField("Further Description of Student Needs")
    gradeLevel = models.CharField(max_length=100)
    preferredPlatform = models.CharField(default="Zoom", max_length=100)

    # Personal Information
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)

    # Useful Functions
    def was_in_the_past(self):
        return self.date < timezone.now().date()

    def is_today(self):
        return self.date == timezone.now().date()

    def has_tutor(self):
        return self.tutor is not None
