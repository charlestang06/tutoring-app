from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "admin@example.com"
        new_password = get_random_string(10)
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(username="admin", email=email, password=new_password)
                self.stdout.write("=======================")
                self.stdout.write("Username: admin")
                self.stdout.write(f"Email: {email}")
                self.stdout.write(f"Password: {new_password}")
                self.stdout.write("=======================")
            else:
                self.stdout.write("Superuser already exists. Skipping...")
        except Exception as e:
            self.stdout.write(str(e))
            self.stdout.write("Failed to create superuser.")