from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .backends import TutorBackend
from .models import *

# Create your views here.

## index.html
def index(request):
    tutoringSessionList = TutoringSession.objects.order_by('date')
    context = {
        "tutoringSessionList": tutoringSessionList,
    }
    return render(request, "tutoring_student/index.html", context)

def tutorView(request):
    tutoringSessionList = TutoringSession.objects.order_by('date')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    user = TutorBackend().authenticate(request, username=email, password=password)
    if user:
        login(request, user, backend='tutoring_student.backends.TutorBackend')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    context = {
        "tutoringSessionList": tutoringSessionList,
        "user" : request.user.is_authenticated,
    }
    return render(request, "tutoring_student/tutorView.html", context)

def tutor_logout(request):
    logout(request)
    return tutorView(request)
    
def student_details(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    tutoringSessionList = []
    if student is None:
        raise Http404("Student does not exist")
    else:
        tutoringSessionList = TutoringSession.objects.filter(student = student).order_by('date')
    return render(request, "tutoring_student/student_details.html", {"student": student, "tutoringSessionList" : tutoringSessionList})

def tutor_details(request, tutor_id):
    return HttpResponse("You're looking at the details of tutor %s." % tutor_id)

def session_details(request, session_id):
    return HttpResponse("You're looking at the details of session %s." % session_id)

def registerSession(request):
    # from registration form
    name = request.POST['name']
    email = request.POST['email']
    date = request.POST['date']
    time = request.POST['time']
    duration = request.POST['duration']
    topic = request.POST['topic']
    description = request.POST['description']
    gradeLevel = request.POST['gradeLevel']
    preferredPlatform = request.POST['preferredPlatform']
    
    student = Student.objects.filter(studentName__contains = name).first()
    if student is None:
        # Create User
        user = User.objects.create_user(username=email,
                                 email=email,
                                 password="123456")
        user.save()
        
        # Create tutor object
        student = Student(user=user, studentName=name, email=email)
        
        student.save()
            
    t = TutoringSession(date=date, time=time, duration=duration, subject=topic, description=description, gradeLevel=gradeLevel, preferredPlatform=preferredPlatform, student=student)
    if not TutoringSession.objects.filter(date__contains = date, time__contains = time, student = student).first() is None:
        return render(request, "tutoring_student/registerSession.html", {"tutoringSession": t, "error_message": "You already registered for a session at this time."})
    else:
        t.save()
        return render(request, "tutoring_student/registerSession.html", {"tutoringSession": t})

