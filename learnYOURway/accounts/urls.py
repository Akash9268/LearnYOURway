from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register,name="register"),
    path('teacher_register/',views.teacher_register.as_view(),name="teacher_sign_up"),
    path('student_register/',views.Student_register.as_view(),name="Student_sign_up"),


]
