from datetime import datetime, timedelta
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import send_html_mail
from .backends import TutorBackend, StudentBackend
from .models import *


##### HELPER FUNCTIONS #####
def check_tutor(user):
    """
    Tutor check function

    Args:
        user (Django user): passed from request object

    Returns:
        bool: True if user is a tutor, False otherwise
    """
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
    """
    Student check function

    Args:
        user (Django user): passed from request object

    Returns:
        bool: True if user is a student, False otherwise
    """
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
    """
    Tutor logout function

    Args:
        request (Django HTTP request): passed from previous view

    Returns:
        HTTP response: redirect to tutorView
    """
    logout(request)
    return tutorView(request)


def student_logout(request):
    """Student logout function

    Args:
        request (Django HTTP Request): passed from previous view

    Returns:
        HTTP response: redirect to studentView
    """
    logout(request)
    return studentView(request)


def get_tutor(request, user):
    """Get tutor object from request or user

    Args:
        request (Django HTTP request): passed from previous view
        user (Django user object): passed from previous view

    Returns:
        Tutor: tutor object if user is a tutor, None otherwise
    """
    tutor = None
    if check_tutor(user) or (check_tutor(request.user)):
        tutor = Tutor.objects.get(user=request.user)
    return tutor


def get_all_tutoring_sessions():
    """Get list of all tutoring sessions

    Returns:
        List: list of all tutoring sessions ordered by date (in ascending order)
    """
    tutoringSessionList = TutoringSession.objects.order_by("date")
    return tutoringSessionList


def get_tutoring_session_student(student):
    """Get list of tutoring sessions for a student

    Args:
        student (Student): student object

    Returns:
        List: list of tutoring sessions for the student ordered by date (in ascending order)
    """
    tutoringSessionList = TutoringSession.objects.filter(student=student).order_by(
        "date"
    )
    return tutoringSessionList


def get_tutoring_session_tutor(tutor):
    """Get list of tutoring sessions for a tutor

    Args:
        tutor (Tutor): tutor object

    Returns:
        List: list of tutoring sessions for the tutor ordered by date (in ascending order)
    """
    tutoringSessionList = TutoringSession.objects.filter(tutor=tutor).order_by("date")
    return tutoringSessionList


def get_events(tutoringSessionList):
    """Get list of events for calendar

    Args:
        tutoringSessionList (List): list of all tutoring sessions ordered by date

    Returns:
        List: list of events for calendar
    """
    events = []
    for session in tutoringSessionList:
        event = {
            "title": f"{session.student.studentName} - {session.subject}",
            "start": f"{session.date}T{session.time}",
            "end": f"{session.date}T{session.time}",
            "className": "taken-session" if session.tutor else "available-session",
            "url": session.id,
        }
        events.append(event)
    return events


def send_confirmation_email(context, email):
    """Send confirmation email through Email backend

    Args:
        context (dict): context dictionary for email template
        email (string): email address of the recipient
    """
    html = loader.render_to_string("tutoring_student/sessionConfirmation.html", context)
    send_html_mail(
        "Iridium Tutoring | Tutoring Session Confirmation",
        html,
        [email],
        "noreply@iridiumtutoring.org",
    )


#### VIEWS ####


def index(request):
    """Index view

    Args:
        request (Django HTTP request): passed from previous view

    Returns:
        index: render index.html with context
    """
    context = {
        "tutoringSessionList": get_all_tutoring_sessions(),
        "minDate": str(
            (datetime.datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        ),
        "maxDate": str(
            (datetime.datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        ),
    }
    request.session["index"] = True
    return render(request, "tutoring_student/index.html", context)


def tutorView(request):
    """Tutor view

    Args:
        request (Django HTTP request): passed from previous view

    Returns:
        tutorView: render tutorView.html with context
    """
    tutoringSessionList = get_all_tutoring_sessions()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    error = ""
    user = TutorBackend().authenticate(request, email=email, password=password)
    if user:
        login(request, user, backend="tutoring_student.backends.TutorBackend")
    elif email == "" and password == "":
        error = "Enter your tutor credentials"
    elif email != "" and password != "":
        error = "Invalid email or password"
    tutor = get_tutor(request, user)

    context = {
        "tutoringSessionList": tutoringSessionList,
        "user": tutor != None,
        "error": error,
        "tutor": tutor,
        "events": get_events(tutoringSessionList),
    }

    return render(request, "tutoring_student/tutorView.html", context)


def studentView(request):
    """Student view

    Args:
        request (Django HTTP request): passed from previous view

    Returns:
        studentView: render studentView.html with context
    """
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
    elif email != "" and name != "":
        error = "Invalid email and full name combination"

    student = None
    if check_student(request.user):
        student = Student.objects.get(user=request.user)
        tutoringSessionList = get_tutoring_session_student(student)

    context = {
        "tutoringSessionList": tutoringSessionList,
        "student": student,
        "user": student != None,
        "error": error,
    }
    return render(request, "tutoring_student/studentView.html", context)


@user_passes_test(check_tutor)
def student_details(request, student_id):
    """Student details view

    Args:
        request (Django HTTP request): passed from previous view
        student_id (int): foreign key for student object

    Raises:
        Http404: if student does not exist or tutor is not authorized

    Returns:
        student_details: render student_details.html with context
    """
    student = get_object_or_404(Student, pk=student_id)
    tutor = get_tutor(request, request.user)
    tutoringSessionList = []
    if student is None:
        raise Http404("Student does not exist")
    else:
        tutoringSessionList = get_tutoring_session_student(student)
    context = {
        "student": student,
        "tutoringSessionList": tutoringSessionList,
        "user": tutor != None,
    }
    return render(request, "tutoring_student/student_details.html", context)


@user_passes_test(check_student)
def session_details_student(request, session_id):
    """Session details view for student

    Args:
        request (Django HTTP request): passed from previous view
        session_id (int): foreign key for tutoring session object

    Raises:
        Http404: if session does not exist or student is not authorized

    Returns:
        session_details_student: render session-student.html with context
    """
    session = get_object_or_404(TutoringSession, pk=session_id)
    if session is None:
        raise Http404("Session does not exist")

    # Cancel button behavior
    if request.method == "POST":
        cancel = request.POST.get("cancel", "")
        if cancel == "True":
            try:
                session.delete()
            except:
                raise Http404("There was an error canceling the session.")
            return redirect("tutoring_student:studentView")
    context = {"tutoringSession": session}
    return render(request, "tutoring_student/session-student.html", context)


@user_passes_test(check_tutor)
def session_details_tutor(request, session_id):
    """Session details view for tutor

    Args:
        request (Django HTTP request): passed from previous view
        session_id (id): foreign key for tutoring session object

    Raises:
        Http404: if session does not exist or tutor is not authorized

    Returns:
        session_details_tutor: render session-tutor.html with context
    """
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        raise Http404("You are not authorized to access this page.")
    try:
        session = get_object_or_404(TutoringSession, pk=session_id)
    except:
        raise Http404("Session does not exist")
    if request.method == "POST":
        claim = request.POST.get("claim", "")
        if claim == "True":
            session.tutor = tutor
        elif claim == "False":
            session.tutor = None
        session.save()

    context = {"tutoringSession": session, "tutor": tutor}
    return render(request, "tutoring_student/session-tutor.html", context)


@user_passes_test(check_tutor)
def tutorProfile(request):
    """Tutor profile view

    Args:
        request (Django HTTP request): passed from previous view

    Returns:
        tutorProfile: render tutorProfile.html with context
    """
    try:
        tutor = get_tutor(request, request.user)
        tutoringSessions = get_tutoring_session_tutor(tutor)
    except:
        raise Http404("You are not authorized to access this page.")
    context = {
        "tutor": tutor,
        "tutoringSessions": tutoringSessions,
        "user": tutor != None,
        "hours": len(tutoringSessions) * 1.5,
    }
    return render(request, "tutoring_student/tutorProfile.html", context)


def sessionConfirmation(request):
    """
    Session confirmation view

    Args:
        request (Django HTTP request): passed from previous view

    Returns:
        sessionConfirmation: render sessionConfirmation.html with context
    """
    # Check if previous page was index
    if "index" in request.session:
        del request.session["index"]
    else:
        raise Http404("You are not authorized to access this page.")

    # Registration form
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    date = request.POST.get("date", "").strip()
    time = request.POST.get("time", "").strip()
    duration = request.POST.get("duration", 1).strip()
    topic = request.POST.get("topic", "").strip()
    description = request.POST.get("description", "").strip()
    gradeLevel = request.POST.get("gradeLevel", "").strip()
    preferredPlatform = request.POST.get("preferredPlatform", "").strip()
    # sendMail = True if request.POST.get("sendMail", "") == "on" else False

    student = Student.objects.filter(
        studentName__contains=name, email__contains=email
    ).first()

    # Create student if not exists
    if student is None:
        # Create user
        user = User.objects.create_user(username=email, email=email, password="123456")
        user.save()

        # Create student object
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

    # Check if session is duplicated
    if (
        not TutoringSession.objects.filter(
            date__contains=date, time__contains=time, student=student
        ).first()
        is None
    ):
        context["error_message"] = "You already registered for a session at this time."
    # Send confirmation email and save tutoring session object
    else:
        try:
            send_confirmation_email(context, email)
            t.save()
        except:
            context["error_message"] = (
                "There was an error confirming the session or sending the email. Try again or contact us for support."
            )
    context["button"] = True
    return render(request, "tutoring_student/sessionConfirmation.html", context)
