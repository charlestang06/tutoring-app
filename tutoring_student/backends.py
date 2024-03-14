# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Tutor, Student

class TutorBackend(ModelBackend):
    """TutorBackend: Custom authentication backend for Tutor model

    Args:
        ModelBackend (Backend): Django ModelBackend
    """
    # Authentication function for Tutor Model
    def authenticate(self, request, email=None, password=None, **kwargs):
        """Authenticate the tutor using email and password

        Args:
            request (Django HTTP request): passed from view
            email (email, optional): email of the tutor. Defaults to None.
            password (string, optional): password of the tutor. Defaults to None.

        Returns:
            User: returns the user if the tutor exists and password is correct, otherwise None
        """
        # Check if the tutor exists 
        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return None
        # Check if provided password is correct
        if tutor.user.check_password(password):
            return tutor.user
        return None


class StudentBackend(ModelBackend):
    """StudentBackend: Custom authentication backend for Student model

    Args:
        ModelBackend (Backend): Django ModelBackend
    """
    # Authentication function for Student Model
    def authenticate(self, request, fullName=None, email=None, password=None, **kwargs):
        """Authenticate the student using full name and email

        Args:
            request (Django HTTP request): passed from view
            email (email, optional): email of the student. Defaults to None.
            fullName (string, optional): full name of the student. Defaults to None.

        Returns:
            User: returns the user if the student exists and credentials are correct, otherwise None
        """
        # Check if the student exists
        try:
            student = Student.objects.get(
                studentName=fullName, email=email
            )
            if not student is None:
                return student.user
            return None
        except Student.DoesNotExist:
            return None
