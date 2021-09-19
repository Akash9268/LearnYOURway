from django.contrib.auth.forms import UserCreationForm
from accounts.models import User,Teacher,Student
from django.db import transaction
from django import forms


class TeacherSignupForm(UserCreationForm):
	Highest_qualification = forms.CharField(required=True)
	Description = forms.CharField(required=True)
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username', 'first_name', 'last_name',)

	@transaction.atomic
	def save(self,commit=True):
		user = super().save(commit=False) #creating the instance of the form
		user.is_teacher = True
		if commit:
			user.save()
		teacher = Teacher.objects.create(user=user)
		teacher.Highest_qualification = self.cleaned_data["Highest_qualification"]
		teacher.Description = self.cleaned_data["Description"]
		teacher.save()
		return user

class StudentSignupForm(UserCreationForm):
	phone_no = forms.CharField(required=True)
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username', 'first_name', 'last_name',)

	@transaction.atomic
	def save(self,commit=True):
		user = super().save(commit=False) #creating the instance of the form
		user.is_student = True
		if commit:
			user.save()
		student = Student.objects.create(user=user)
		student.phone_no = self.cleaned_data["phone_no"]
		student.save()
		return user

