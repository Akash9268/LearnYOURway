from django.urls import include,path
from . import views
urlpatterns = [
    path('',views.register,name="register"),
    path('teacher_dash/<str:pk>',views.teacher_dash,name='teacher_dash'),
    path('student_dash/<str:pk>',views.student_dash,name='student_dash'),
    path('logout/',views.logout_view,name='logout_view'),
    path('teacher_login_register',views.teacher_login_or_register,name='teacher_login_register'),
    path('student_login_register',views.student_login_or_register,name='student_login_register'),

]
