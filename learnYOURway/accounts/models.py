from django.db import models
from django.contrib.auth.models import AbstractUser  #default fields = firstname, lastname, isstaff.....
# Create your models here.


class User(AbstractUser):
	is_teacher = models.BooleanField(default=False)
	is_student = models.BooleanField(default=False)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)

class Teacher(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key =True)
	department = models.CharField(max_length=100)
	phone_no = models.CharField(max_length=10)

class Student(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key =True)
	roll_no = models.CharField(max_length=100)
	phone_no = models.CharField(max_length=10)



