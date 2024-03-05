from django.urls import path

from . import views

app_name = "tutoring_student"

urlpatterns = [
    path("", views.index, name="index"),
    path("tutorPortal", views.tutorView, name="tutorView"),
    path("studentPortal", views.studentView, name="studentView"),
    path("tutorLogout", views.tutor_logout, name="tutor_logout"),
    path("studentLogout", views.student_logout, name="student_logout"),
    path("student/<int:student_id>/", views.student_details, name="student_details"),
    path("tutor/<int:tutor_id>/", views.tutor_details, name="tutor_details"),
    path("session/<int:session_id>/", views.session_details, name="session_details"),
    path("session-confirmation/", views.sessionConfirmation, name="register_session"),
]
