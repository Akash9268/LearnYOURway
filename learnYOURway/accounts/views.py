from __future__ import print_function
import os.path
from google import auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
from django.http import HttpResponse
import requests

from learning.forms import CourseForm

import json
import os

from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Teacher,Student
from .forms import TeacherSignupForm,StudentSignupForm
from learning.models import Course
# Create your views here.

import config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses','https://www.googleapis.com/auth/classroom.rosters']

from django.shortcuts import render
import os



def logout_view(request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect('/')


def register(request):
    return render(request,'register.html')


def teacher_dash(request,pk):
    user = get_object_or_404(User,pk=pk)
    course_list = Course.objects.filter(taught_by=pk)
    return render(request,'teacher_dash.html',{"user":user,"course_list":course_list})


def student_dash(request,pk):
    user = get_object_or_404(User,pk=pk)
    return render(request,'student_dash.html',{"user":user})


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
                    creds = None
                    # The file token.json stores the user's access and refresh tokens, and is
                    # created automatically when the authorization flow completes for the first
                    # time.
                    if os.path.exists('token.json'):
                        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                    # If there are no (valid) credentials available, let the user log in.
                    if not creds or not creds.valid:
                        if creds and creds.expired and creds.refresh_token:
                            creds.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file(
                                'credentials.json', SCOPES)
                            creds = flow.run_local_server(port=0)
                        # Save the credentials for the next run
                        with open('token.json', 'w') as token:
                            token.write(creds.to_json())
                    config.service = build('classroom', 'v1', credentials=creds)
                    
                    return redirect('teacher_dash', pk=user.pk)
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        elif request.POST.get('submit') == 'register':
            form = TeacherSignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request,user)
                messages.success(request,'Registration successful.')
                return redirect('/')
            messages.error(request,'Unsuccessful registration, Invalid Information')

    register_form = TeacherSignupForm()
    login_form = AuthenticationForm()
    return render(request,template_name='teacher_register.html',context={'login_form':login_form,'register_form':register_form})


def student_login_or_register(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user.is_student is False:
                    messages.error(request, "Invalid username.")
                elif user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('student_dash', pk=user.pk)
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        elif request.POST.get('submit') == 'register':
            form = StudentSignupForm(request.POST)
            if form.is_valid():
                print("Hello")
                user = form.save()
                login(request,user)
                messages.success(request,'Registration successful.')
                return redirect('/')
            messages.error(request,'Unsuccessful registration, Invalid Information')
    register_form = StudentSignupForm()
    login_form = AuthenticationForm()
    return render(request,template_name='student_register.html',context={'login_form':login_form,'register_form':register_form})