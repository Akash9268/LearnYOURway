from .models import Course
from django.db import transaction
from django import forms
from django.forms import ModelForm


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'