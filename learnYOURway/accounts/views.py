from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import User,Teacher,Student
from .forms import TeacherSignupForm,StudentSignupForm
from learning.models import Course
# Create your views here.


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')


def register(request):
    return render(request,'register.html')


def teacher_dash(request,pk):
    user = get_object_or_404(User,pk=pk)
    course_list = Course.objects.filter(taught_by=pk)
    return render(request,'teacher_dash.html',{"user":user,"course_list":course_list})


def student_dash(request,pk):
    user = get_object_or_404(User,pk=pk)
    return render(request,'student_dash.html',{user:user})


class teacher_register(CreateView):
    model = User
    form_class = TeacherSignupForm
    template_name = 'teacher_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def validate(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('/')

    def get_success_url(self):
        return reverse('register')


class Student_register(CreateView):
    model = User
    form_class = StudentSignupForm
    template_name = 'student_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def validate(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('/')

    def get_success_url(self):
        return reverse('register')


def teacher_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user.is_teacher is False:
                messages.error(request,"Invalid username.")
            elif user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('teacher_dash',pk=user.pk)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="teacher_login.html", context={"login_form": form})


def student_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user.is_student is False:
                messages.error(request,"Invalid username.")
            elif user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('base_page',pk=user.pk)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="student_login.html", context={"login_form": form})


def teacher_login_or_register(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user.is_teacher is False:
                    messages.error(request, "Invalid username.")
                elif user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('teacher_dash', pk=user.pk)
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        elif request.POST.get('submit') == 'register':
            form = TeacherSignupForm(request.POST)
            if form.is_valid():
                user = form.save();
                login(request,user);
                messages.success(request,'Registration successful.')
                return redirect('/')
            messages.error(request,'Unsuccessful registration, Invalid Information')

    register_form = TeacherSignupForm()
    login_form = AuthenticationForm()
    return render(request,template_name='teacher_register.html',context={'login_form':login_form,'register_form':register_form})
