import django_filters
from learning.models import Course

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = ('taught_by','tag')