from django.urls import path

from . import views

app_name = "tutoring_student"

urlpatterns = [
    path("studentView", views.index, name="index"),
    path("tutorView", views.tutorView, name="tutorView"),
     path("tutorLogout", views.tutor_logout, name="tutor_logout"),
    path("student/<int:student_id>/", views.student_details, name="student_details"),
    path("tutor/<int:tutor_id>/", views.tutor_details, name="tutor_details"),
    path("session/<int:session_id>/", views.session_details, name="session_details"),
    path("registerSession/", views.registerSession, name="register_session"),
]