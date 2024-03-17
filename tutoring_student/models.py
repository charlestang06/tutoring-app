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
        return self.student.studentName + " - " + str(self.date)

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
    isRecurring = models.BooleanField(default=False)

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


class RecurringSession(models.Model):
    """
    Model for recurring session
    """

    def __str__(self):
        return (
            self.student.studentName
            + " - "
            + self.tutor.tutorName
            + " - "
            + self.dayOfWeek
        )

    # Recurring session information
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    sessions = models.ManyToManyField(TutoringSession, default=[], blank=True)  # all sessions related to this recurring
    dayOfWeek = models.CharField(max_length=10)
    time = models.TimeField("Time of Session")
    startDate = models.DateField("Starting Date")
    endDate = models.DateField("Ending Date")
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

    def was_in_the_past(self):
        """Tests if the recurring sessions has ended

        Returns:
            bool: True if the recurring session has ended, False otherwise
        """
        return self.endDate < timezone.now().date()

    def generate_sessions(self):
        """Generate all sessions for the recurring session given startDate and endDate and daysOfWeek

        Returns:
            bool: True if sessions have been generated successfully
        """
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        assert self.dayOfWeek in days
        try:
            self.generate_sessions_helper(day=days.index(self.dayOfWeek))
            return True
        except:
            return False

    def generate_sessions_helper(self, day):
        """Helper function to generate all sessions for the recurring session given a day of the week

        Args:
            day (int): day of the week, 0 for Monday, 1 for Tuesday, ..., 6 for Sunday

        Returns:
            bool: True if sessions have been generated successfully
        """
        start = datetime.datetime.strptime(self.startDate, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(self.endDate, "%Y-%m-%d").date()
        while start <= end:
            if start.weekday() == day:
                session = TutoringSession(
                    date=start,
                    time=self.time,
                    duration=self.duration,
                    subject=self.subject,
                    description=self.description,
                    gradeLevel=self.gradeLevel,
                    preferredPlatform=self.preferredPlatform,
                    student=self.student,
                    tutor=self.tutor,
                    isRecurring=True,
                )
                session.save()
                self.sessions.add(session)
            start += datetime.timedelta(days=1)
        return True
