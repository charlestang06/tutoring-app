import random
from django.test import TestCase, Client
from django.utils import timezone
from .models import *
import datetime

# Create your tests here.

class TutoringSessionModelTest(TestCase):
    def setUp(self):
        self.form_data = {
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'duration': random.randint(1, 3) / 2,
            'topic': "Math",
            'description': "Help with math, more specifically: Algebra 2 and Trigonometry.",
            'gradeLevel': "10",
            'preferredPlatform': "Google Meet",
            'name': "  John Doe  ",
            'email': "johndoe@gmail.com ",
        }
        
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

    def test_register_session_form_not_from_index(self):
        """
        Test the form for registering a tutoring session from index page
        """
        response = self.client.post("/session-confirmation/", self.form_data)
        # did not come from index page
        self.assertEqual(response.status_code, 404)
        
    def test_register_session_form_from_index(self):
        """
        Test the form for registering a tutoring session from index page
        """
        response1 = self.client.post("/")
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post("/session-confirmation/", self.form_data)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(Student.objects.filter(studentName__contains="John Doe")), 1)
        self.assertEqual(len(TutoringSession.objects.filter(date=self.form_data['date'], time=self.form_data['time'], duration=self.form_data['duration'], subject=self.form_data['topic'])), 1)
