from django.test import TestCase
from django.utils import timezone
from .models import *
import datetime

# Create your tests here.

class TutoringSessionModelTest(TestCase):
    def test_was_in_past_with_future_date(self):
        """
        was_in_the_past() returns False for sessions in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_session = TutoringSession(date = time.date(), time=timezone.now().time(), duration=1, subject="Math", description="Help with math",
                                         gradeLevel="12", preferredPlatform="Zoom",
                                         student=Student(studentName="John Doe", email="johndoe@gmail.com"))
        self.assertIs(future_session.was_in_the_past(), False)

    def test_was_in_past_with_past_date(self):
        """
        was_in_the_past() returns True for sessions in the past.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        past_session = TutoringSession(date = time.date(), time=timezone.now().time(), duration=1, subject="Math", description="Help with math",
                                       gradeLevel="12", preferredPlatform="Zoom",
                                       student=Student(studentName="John Doe", email="johndoe@gmail.com"))
        self.assertIs(past_session.was_in_the_past(), True)
