from rest_framework import serializers
from accounts.models import Teacher

class TeacherSerializer(serializers.Serializer):
    class Meta:
        model = Teacher
        fields = ('Highest_qualification','Description')



