from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
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
    password = request.POST.get('password','')
    print(password)
    context = {
        "tutoringSessionList": tutoringSessionList,
        "password": password,
    }
    return render(request, "tutoring_student/tutorView.html", context)
    
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
        student = Student(studentName=name, email=email)
        student.save()
    
    # tutor =  Tutor.objects.filter(tutorName__contains = "Charles") | Tutor.objects.first()
    
    t = TutoringSession(date=date, time=time, duration=duration, subject=topic, description=description, gradeLevel=gradeLevel, preferredPlatform=preferredPlatform, student=student)
    if not TutoringSession.objects.filter(date__contains = date, time__contains = time, student = student).first() is None:
        return render(request, "tutoring_student/registerSession.html", {"tutoringSession": t, "error_message": "You already registered for a session at this time."})
    else:
        t.save()
        return render(request, "tutoring_student/registerSession.html", {"tutoringSession": t})

