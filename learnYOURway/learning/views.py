from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from .forms import CourseForm
from accounts.models import Teacher
from learning.filters import CourseFilter
from learning.models import Course
from accounts.models import Student
# Create your views here.

def add_course(request,pk):
    teacher = get_object_or_404(Teacher,pk=pk)
    if request.method == "POST":
        form = CourseForm(teacher,request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dash',pk=pk)
    else:
        form = CourseForm(teacher)

    return render(request,'course_form.html',{'form' : form,'teacher' : teacher})

    
def course_list(request,pk):
    student = get_object_or_404(Student, pk=pk)
    courses = Course.objects.all()
    myFilter = CourseFilter(request.GET,queryset=courses)
    courses = myFilter.qs
    return render(request,'course_list.html',{"courses":courses,"myFilter":myFilter,"student":student})


def add_course(request,pk,pk2):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, pk=pk2)
    student.courses.add(course)
    student.save()

    return redirect('/')

def wishlist(request,pk):
    student = get_object_or_404(Student,pk=pk)
    courses = student.courses.all()
    return render(request,'Wishlist.html',{"courses":courses,"student":student})

def remove_course(request,pk,pk2):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, pk=pk2)
    student.courses.remove(course)
    return redirect('/')



