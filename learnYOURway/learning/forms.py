from django.db.models.query import QuerySet
from .models import Course
from django.db import transaction
from django import forms
from django.forms import ModelForm
from accounts.models import Teacher


class CourseForm(forms.ModelForm):
    def __init__(self,teacher,*args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['taught_by'] = forms.ModelChoiceField(initial=teacher.pk,queryset=Teacher.objects.filter(pk=teacher.pk))

    class Meta:
        model = Course
        fields = ('__all__')


