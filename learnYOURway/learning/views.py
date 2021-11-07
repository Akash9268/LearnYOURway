from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import CourseForm
from accounts.models import Teacher
from learning.filters import CourseFilter
from learning.models import Course
from accounts.models import User, Student, Order, CourseOrder
import razorpay
import requests
import json
from learnYOURway.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
import config
import accounts.views
# Create your views here.

def add_course_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = CourseForm(teacher, request.POST)
        if form.is_valid():
            course = {
                'name': form.cleaned_data.get("Subject_name"),
                'description': form.cleaned_data.get("Description"),
                'ownerId': 'me',
                'courseState': 'PROVISIONED'
            }

            course = config.service.courses().create(body=course).execute()

            obj = form.save(commit=False)
            obj.Course_id = course.get('id')
            obj.save()

            messages.info(request, 'Courses Added and Google Classroom Has been created successfully! Check Now !!!')
            return redirect('teacher_dash', pk=pk)
    else:
        form = CourseForm(teacher)

    return render(request, 'course_form.html', {'form': form, 'teacher': teacher})


def course_desc(request, pk, pk2):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, pk=pk2)
    courses = student.courses.all()
    ispresent = student.courses.filter(pk=pk)

    if ispresent.exists():
        return render(request, 'Wishlist.html', {"courses": courses, "student": student})

    cost = float(course.Course_fee);
    user = get_object_or_404(User, pk=pk2)
    context = {
        'amount': cost,
        'course': course,
        'student': student,
        'user': user,
    }
    return render(request, 'course_desc.html', context)


def payment(request, pk, pk2):
    student = get_object_or_404(Student, pk=pk)
    course = get_object_or_404(Course, pk=pk2)
    user = get_object_or_404(User, pk=pk)
    order = Order.objects.create(student=student, total_amount=0)
    course_in_order = CourseOrder.objects.create(order=order, course=course, price=course.Course_fee)
    order.total_amount = course.Course_fee
    order.save()
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    order_currency = 'INR'

    callback_URL = 'http://127.0.0.1:8000/' + "handlerequest/" + str(pk)+'/'+str(pk2)
    print(callback_URL)
    DATA = {
        "amount": order.total_amount * 100.00,
        "currency": 'INR',
        "receipt": order.order_id,
        'payment_capture': '0'
    }
    payment_order = client.order.create(data=DATA)
    print(payment_order['id'])
    order.razorpay_order_id = payment_order['id']
    order.save()
    print(order.order_id)
    cost = float(order.total_amount)
    context = {
        'order': order,
        'amount': cost,
        'course': course,
        'student': student,
        'user': user,
        'api_key': RAZORPAY_API_KEY,
        'razorpay_order_id': order.razorpay_order_id,
        'callbackURL': callback_URL,
        'order_id': order.order_id,
        'student':student,
        'course':course
        
    }
    messages.info(request, 'Order created')
    return render(request, 'payment_summary.html', context)

@csrf_exempt
def handlerequest(request,pk1,pk2):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
            result = client.utility.verify_payment_signature(params_dict)
            if result == None:
                amount = order_db.total_amount * 100
                print(amount)
                payment_currency = "INR"
                try:
                    check = client.payment.capture(payment_id, amount,{"currency":"payment_currency"})
                    order_db.payment_status = 1
                    order_db.save()

                    course = get_object_or_404(Course, pk=pk2)
                    student = get_object_or_404(Student, pk=pk1)
                    student.courses.add(course)
                    student.save()


                    if request.user.is_authenticated:
                        data = json.load(open('token.json'),)
                        headers = {
                                    'Authorization': 'Bearer ' + data['token'],
                                    'Content-Type': 'application/json'
                                }
                        data = {
                            'courseId': course.Course_id,
                            'id': 'me',
                            'role': 'STUDENT',
                            'userId': student.user.email_id
                        }

                        response = requests.post("https://classroom.googleapis.com/v1/invitations",json=data,headers=headers)
                        print(response.text)
                    else:
                        print("NOT VALID")

                    return render(request, 'success.html', {'id': order_db.id})
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    print("Fail1")
                    return render(request, 'fail.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                print("Fail2")
                return render(request, 'fail.html')
        except:
            return HttpResponse("505 not found")


def course_list(request, pk):
    student = get_object_or_404(Student, pk=pk)
    courses = Course.objects.all()
    myFilter = CourseFilter(request.GET, queryset=courses)
    courses = myFilter.qs
    user = get_object_or_404(User, pk=pk)
    return render(request, 'course_list.html',
                  {"courses": courses, "myFilter": myFilter, "student": student, "user": user})

def wishlist(request, pk):
    student = get_object_or_404(Student, pk=pk)
    courses = student.courses.all()
    return render(request, 'Wishlist.html', {"courses": courses, "student": student})


def remove_course(request, pk, pk2):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, pk=pk2)
    user = get_object_or_404(User, pk=pk2)
    student.courses.remove(course)
    context = {
        'course': course,
        'student': student,
        'user': user
    }
    return render(request, 'student_dash.html', context)
