from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from .forms import CourseForm
from django.forms.models import model_to_dict
from accounts.models import Teacher
from django.views.generic import CreateView,FormView
# Create your views here.

def add_course(request,pk):
    teacher = get_object_or_404(Teacher,pk=pk)
    if request.method == "POST":
        form = CourseForm(teacher,request.POST)
        print("hello")
        if form.is_valid():
            print("hello2")
            form.save()
            return redirect('teacher_dash',pk=pk)
    else:
        form = CourseForm(teacher)

    return render(request,'course_form.html',{'form' : form,'teacher' : teacher})