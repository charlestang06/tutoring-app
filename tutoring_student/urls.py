from django.urls import path

from . import views

app_name = "tutoring_student"

urlpatterns = [
    path("", views.index, name="index"),
    path("tutorPortal", views.tutorView, name="tutorView"),
    path("studentPortal", views.studentView, name="studentView"),
    path("office-hours", views.officeHours, name="officeHours"),
    path("tutorPortal/tutorLogout", views.tutor_logout, name="tutor_logout"),
    path("studentPortal/studentLogout", views.student_logout, name="student_logout"),
    path("tutorPortal/student/<int:student_id>/", views.student_details, name="student_details"),
    path("studentPortal/session-student/<int:session_id>/", views.session_details_student, name="session_details_student"),
    path("tutorPortal/session-tutor/<int:session_id>/", views.session_details_tutor, name="session_details_tutor"),
    path("tutorPortal/profile", views.tutorProfile, name="tutorProfile"),
    path("tutorPortal/utilities", views.tutorUtilities, name="tutorUtilities"),
    path("tutorPortal/utilities/recurrings", views.tutorRecurrings, name="tutorRecurrings"),
    path("tutorPortal/utilities/recurrings/<int:recurring_id>/", views.recurring_details, name="recurring_details"),
    path("session-confirmation/", views.sessionConfirmation, name="register_session"),
]
