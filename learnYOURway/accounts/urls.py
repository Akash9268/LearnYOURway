from django.urls import path
from . import views
urlpatterns = [
    path('',views.register,name="register"),
    path('teacher_register/',views.teacher_register.as_view(),name="teacher_sign_up"),
    path('student_register/',views.Student_register.as_view(),name="Student_sign_up"),
    path('teacher_login/',views.teacher_login,name="teacher_login"),
    path('student_login/',views.student_login,name="student_login"),
    path('teacher_dash/<str:pk>',views.teacher_dash,name='teacher_dash'),
    path('student_dash/<str:pk>',views.student_dash,name='student_dash'),

]
