import random
from django.test import TestCase, Client
from django.utils import timezone
from .models import *
import datetime


class TutoringSessionModelTest(TestCase):
    def setUp(self):
        """
        Set up a tutoring session and form data for testing.
        """
        self.form_data = {
            "date": timezone.now().date(),
            "time": timezone.now().time(),
            "duration": random.randint(1, 3) / 2,
            "topic": "Math",
            "description": "Help with math, more specifically: Algebra 2 and Trigonometry.",
            "gradeLevel": "10",
            "preferredPlatform": "Google Meet",
            "name": "  John Doe  ",
            "email": "johndoe@gmail.com ",
        }
        time = timezone.now()
        self.session = TutoringSession(
            date=time.date(),
            time=timezone.now().time(),
            duration=1,
            subject="Math",
            description="Help with math",
            gradeLevel="12",
            preferredPlatform="Zoom",
            student=Student(studentName="John Doe", email="johndoe@gmail.com"),
        )

    def test_was_in_past_with_future_date(self):
        """
        was_in_the_past() returns False for sessions in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_session = self.session
        future_session.date = time.date()
        self.assertIs(future_session.was_in_the_past(), False)

    def test_was_in_past_with_past_date(self):
        """
        was_in_the_past() returns True for sessions in the past.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        past_session = self.session
        past_session.date = time.date()
        self.assertIs(past_session.was_in_the_past(), True)

    def test_is_today(self):
        """
        is_today() returns True for sessions that are today.
        """
        time = timezone.now()
        today_session = TutoringSession(
            date=time.date(),
            time=timezone.now().time(),
            duration=1,
            subject="Math",
            description="Help with math",
            gradeLevel="12",
            preferredPlatform="Zoom",
            student=Student(studentName="John Doe", email="johndoe@gmail.com"),
        )
        self.assertIs(today_session.is_today(), True)

    def test_has_tutor(self):
        """
        has_tutor() returns True for sessions that have a tutor object in its field.
        """
        time = timezone.now()
        session = TutoringSession(
            date=time.date(),
            time=timezone.now().time(),
            duration=1,
            subject="Math",
            description="Help with math",
            gradeLevel="12",
            preferredPlatform="Zoom",
            student=Student(studentName="John Doe", email="johndoe@gmail.com"),
            tutor=Tutor(tutorName="John Doe", email="johndoe@yahoo.com"),
        )
        self.assertIs(session.has_tutor(), True)

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
        self.assertEqual(
            len(Student.objects.filter(studentName__contains="John Doe")), 1
        )
        self.assertEqual(
            len(
                TutoringSession.objects.filter(
                    date=self.form_data["date"],
                    time=self.form_data["time"],
                    duration=self.form_data["duration"],
                    subject=self.form_data["topic"],
                )
            ),
            1,
        )


class RecurringSessionModelTest(TestCase):
    def setUp(self):
        """
        Set up a recurring session for testing.
        """
        time = timezone.now()
        student = Student(studentName="John Student", email="johndoe@gmail.com")
        tutor = Tutor(tutorName="John Tutor", email="johndoe@gmail.com")
        self.recurring = RecurringSession(
            student=student,
            tutor=tutor,
            dayOfWeek="Monday",
            time=time.time(),
            startDate=time.date(),
            endDate=time.date() + datetime.timedelta(days=100),
            duration=1,
            subject="Math",
            description="Help with math",
            gradeLevel="12",
            preferredPlatform="Zoom",
        )

    # def test_generate_sessions(self):
    #     """
    #     generate_sessions() returns True for sessions that have been generated.
    #     """
    #     self.assertTrue(self.recurring.generate_sessions())

    def test_was_in_past(self):
        """
        was_in_the_past() returns True for sessions that have ended.
        """
        self.assertIs(self.recurring.was_in_the_past(), False)
        self.recurring.endDate = timezone.now().date() - datetime.timedelta(days=1)
        self.assertIs(self.recurring.was_in_the_past(), True)
