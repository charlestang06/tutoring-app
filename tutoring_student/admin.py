from django.contrib import admin
from .models import Tutor, Student, TutoringSession

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(TutoringSession)
