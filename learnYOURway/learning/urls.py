from django.urls import path
from . import views

urlpatterns = [
    path('course_list/<str:pk>',views.course_list,name="course_list"),
    path('wishlist/<str:pk>',views.wishlist,name='wishlist'),
    path('remove_course/<str:pk>/<str:pk2>',views.remove_course,name='remove_course'),
    path('course_desc/<str:pk>/<str:pk2>',views.course_desc,name='course_desc'),
    path('payment/<str:pk>/<str:pk2>',views.payment,name='payment'),
    path('handlerequest/<str:pk1>/<str:pk2>', views.handlerequest, name='handlerequest'),
    path('add_course/<str:pk>/', views.add_course_teacher,name='add_course_teacher'),

]
