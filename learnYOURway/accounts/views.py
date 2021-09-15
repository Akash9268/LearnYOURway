from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse

from .models import User,Teacher,Student
from .forms import TeacherSignupForm,StudentSignupForm
# Create your views here.



def register(request):
	return render(request,'register.html')


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
