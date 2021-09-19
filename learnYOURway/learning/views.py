import re
from django.shortcuts import render
from .serializers import TeacherSerializer
from accounts.models import Teacher

from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['GET'])
def teacher_list(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers,many=True)

    return Response(serializer.data)

@api_view(['POST'])
def create_teacher(request):
    teacher = TeacherSerializer(data = request.data)
    if teacher.is_valid():
        teacher.save()

    return Response(teacher.data)


