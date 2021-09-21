from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from .forms import CourseForm
from django.forms.models import model_to_dict
from accounts.models import Teacher
# Create your views here.

def add_course(request,pk):
    teacher = get_object_or_404(Teacher,pk = pk)
    print(teacher.user.first_name)
    if request.method == "POST":
        form = CourseForm(request.POST,instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dash',pk=pk)
    else:
        data = {'Taught_by':'teacher'}
        form = CourseForm(initial=data)

    return render(request,'course_form.html',{'form' : form})