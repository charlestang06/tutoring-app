from django.contrib import admin
from .models import *

class RecurringInline(admin.TabularInline):
    model = RecurringSession.sessions.through
    
class RecurringAdmin(admin.ModelAdmin):
    """Recurring admin."""
    model = RecurringSession
    inlines = [
        RecurringInline,
    ]
    exclude = ('sessions',)
# Register your models here.
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(TutoringSession)
admin.site.register(RecurringSession, RecurringAdmin)