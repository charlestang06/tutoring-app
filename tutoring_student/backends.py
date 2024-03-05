# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Tutor, Student


# Custom authentication backend for Tutor model
class TutorBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return None

        # Check if the tutor exists and if the provided password is correct
        if tutor.user.check_password(password):
            return tutor.user
        return None


# Custom authentication backend for Student model
class StudentBackend(ModelBackend):
    def authenticate(self, request, fullName=None, email=None, password=None, **kwargs):
        try:
            student = Student.objects.get(
                studentName=fullName, email=email
            )
            if student is None:
                return None
            else:
                return student.user
        except Student.DoesNotExist:
            return None
