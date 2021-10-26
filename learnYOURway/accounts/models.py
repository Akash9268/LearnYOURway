from django.db import models
from django.contrib.auth.models import AbstractUser  #default fields = firstname, lastname, isstaff.....
from django.core.validators import MinLengthValidator
from learning.models import Course
# Create your models here.


class User(AbstractUser):
	is_teacher = models.BooleanField(default=False)
	is_student = models.BooleanField(default=False)
	first_name = models.CharField(max_length=100,blank=False)
	last_name = models.CharField(max_length=100,blank=True)


class Teacher(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key =True)
	Highest_qualification = models.CharField(max_length=100,null=True,blank=True)
	Description = models.TextField(null=True,blank=True,validators=[MinLengthValidator(70)])

	def __str__(self):
		return self.user.first_name

class Student(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key =True)
	courses = models.ManyToManyField(Course)
	phone_no = models.CharField(max_length=10,null=True,blank=True)
	email_id = models.EmailField(max_length=100,null=True, blank=True)





