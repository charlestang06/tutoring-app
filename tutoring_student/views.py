from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import send_html_mail
from .backends import TutorBackend, StudentBackend
from .models import *


# Create your views here.


##### HELPER FUNCTIONS #####
def check_tutor(user):
    if user is None or not user.is_authenticated:
        return False
    else:
        try:
            tutor = Tutor.objects.get(user=user)
            if tutor is not None:
                return True
            else:
                return False
        except Tutor.DoesNotExist:
            return False


def check_student(user):
    if user is None or not user.is_authenticated:
        return False
    else:
        try:
            student = Student.objects.get(user=user)
            if student is not None:
                return True
            else:
                return False
        except Student.DoesNotExist:
            return False

def tutor_logout(request):
    logout(request)
    return tutorView(request)

def student_logout(request):
    logout(request)
    return studentView(request)


#### VIEWS ####

def index(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    password = "123456"
    error = ""
    tutoringSessionList = TutoringSession.objects.order_by("date")
    context = {"tutoringSessionList": tutoringSessionList, "error": error}
    request.session["index"] = True
    return render(request, "tutoring_student/index.html", context)

def tutorView(request):
    tutoringSessionList = TutoringSession.objects.order_by("date")
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    error = ""
    user = TutorBackend().authenticate(request, email=email, password=password)
    if user:
        login(request, user, backend="tutoring_student.backends.TutorBackend")
        # login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    elif email == "" and password == "":
        error = "Enter your tutor credentials"
    elif email != "" and password != "":
        error = "Invalid email or password"

    tutor = None
    if check_tutor(user) or (check_tutor(request.user)):
        tutor = Tutor.objects.get(user=request.user)

    context = {
        "tutoringSessionList": tutoringSessionList,
        "user": check_tutor(request.user),
        "error": error,
        "tutor": tutor,
    }

    return render(request, "tutoring_student/tutorView.html", context)

def studentView(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    password = "123456"
    error = ""
    tutoringSessionList = []
    user = StudentBackend().authenticate(
        request, fullName=name, email=email, password=password
    )

    if user:
        login(request, user, backend="tutoring_student.backends.StudentBackend")
    elif email == "" and name == "":
        error = "Enter your student information"
    elif (email != "" and name != ""):
        error = "Invalid email and full name combination"

    student = None
    if check_student(request.user):
        student = Student.objects.get(user=request.user)
    if student is not None:
        tutoringSessionList = TutoringSession.objects.filter(student=student).order_by(
            "date"
    )

    context = {
        "tutoringSessionList": tutoringSessionList,
        "user": check_student(request.user),
        "error": error,
    }
    return render(request, "tutoring_student/studentView.html", context)

@user_passes_test(check_tutor)
def student_details(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    tutoringSessionList = []
    if student is None:
        raise Http404("Student does not exist")
    else:
        tutoringSessionList = TutoringSession.objects.filter(student=student).order_by(
            "date"
        )
    return render(
        request,
        "tutoring_student/student_details.html",
        {"student": student, "tutoringSessionList": tutoringSessionList},
    )

@user_passes_test(check_student)
def session_details_student(request, session_id):
    session = get_object_or_404(TutoringSession, pk=session_id)
    if session is None:
        raise Http404("Session does not exist")
    context = {"tutoringSession": session}
    return render(request, "tutoring_student/session-student.html", context)

@user_passes_test(check_tutor)
def session_details_tutor(request, session_id):
    tutor = None
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        tutor = None
    session = get_object_or_404(TutoringSession, pk=session_id)
    if session is None:
        raise Http404("Session does not exist")
    if request.method == "POST":
        claim = request.POST.get('claim', '')
        if claim == "True":
            session.tutor = tutor
        elif claim == "False":
            session.tutor = None
        session.save()
    
    context = {"tutoringSession": session, "tutor" : tutor}
    return render(request, "tutoring_student/session-tutor.html", context)


def sessionConfirmation(request):
    if "index" in request.session:
        del request.session["index"]
    else:
        raise Http404("You are not authorized to access this page.")
    # from registration form
    name = request.POST["name"].strip()
    email = request.POST["email"].strip()
    date = request.POST["date"]
    time = request.POST["time"]
    duration = request.POST["duration"].strip()
    topic = request.POST["topic"]
    description = request.POST["description"].strip()
    gradeLevel = request.POST["gradeLevel"].strip()
    preferredPlatform = request.POST["preferredPlatform"]

    student = Student.objects.filter(studentName__contains=name).first()
    if student is None:
        # Create User
        user = User.objects.create_user(username=email, email=email, password="123456")
        user.save()

        # Create tutor object
        student = Student(user=user, studentName=name, email=email)

        student.save()

    t = TutoringSession(
        date=date,
        time=time,
        duration=duration,
        subject=topic,
        description=description,
        gradeLevel=gradeLevel,
        preferredPlatform=preferredPlatform,
        student=student,
    )

    context = {"tutoringSession": t, "error_message": None, "button": False}

    if (
        not TutoringSession.objects.filter(
            date__contains=date, time__contains=time, student=student
        ).first()
        is None
    ):
        context["error_message"] = "You already registered for a session at this time."
    else:
        try:
            html = loader.render_to_string(
                "tutoring_student/sessionConfirmation.html", context
            )
            send_html_mail("Iridium Tutoring | Tutoring Session Confirmation", html, [email], "noreply@iridiumtutoring.org")
            t.save()
        except:
            context["error_message"] = (
                "There was an error confirming the session or sending the email. Try again or contact us for support."
            )
    context["button"] = True
    return render(request, "tutoring_student/sessionConfirmation.html", context)
