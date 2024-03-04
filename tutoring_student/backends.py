# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Tutor

class TutorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            tutor = Tutor.objects.get(user__email=username)
        except Tutor.DoesNotExist:
            return None

        # Check if the tutor exists and if the provided password is correct
        if tutor.user.check_password(password):
            return tutor.user
        return None
