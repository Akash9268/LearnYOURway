from django.urls import path
from . import views

urlpatterns = [
    path('add_course/<str:pk>/', views.add_course,name='add_course'),
]