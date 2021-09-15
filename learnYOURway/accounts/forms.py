from django.contrib.auth.forms import UserCreationForm
from .models import User,Teacher,Student
from django.db import transaction
from django import forms


class TeacherSignupForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self,commit=True):
		user = super().save(commit=False) #creating the instance of the form
		user.is_teacher = True
		if commit:
			user.save()
		teacher = Teacher.objects.create(user=user)
		teacher.save()
		return user

class StudentSignupForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self,commit=True):
		user = super().save(commit=False) #creating the instance of the form
		user.is_student = True
		if commit:
			user.save()
		student = Student.objects.create(user=user)
		student.save()
		return user

