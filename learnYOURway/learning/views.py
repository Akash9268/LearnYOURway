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
from learnYOURway.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.




def course_desc(request, pk, pk2):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, pk=pk2)
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

    callback_URL = 'http://127.0.0.1:8000/' + "handlerequest/"
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
        'order_id': order.order_id
    }
    messages.info(request, 'Order created')
    return render(request, 'payment_summary.html', context)


@csrf_exempt
def handlerequest(request):
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
            print(result)
            print(payment_id)
            if result == None:
                amount = order_db.total_amount * 100
                print(amount)
                payment_currency = "INR"
                try:
                    check = client.payment.capture(payment_id, amount,{"currency":"payment_currency"})
                    order_db.payment_status = 1
                    order_db.save()
                    print("Hi")
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


def add_course_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = CourseForm(teacher, request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dash', pk=pk)
    else:
        form = CourseForm(teacher)

    return render(request, 'course_form.html', {'form': form, 'teacher': teacher})


def course_list(request, pk):
    student = get_object_or_404(Student, pk=pk)
    courses = Course.objects.all()
    myFilter = CourseFilter(request.GET, queryset=courses)
    courses = myFilter.qs
    user = get_object_or_404(User, pk=pk)
    return render(request, 'course_list.html',
                  {"courses": courses, "myFilter": myFilter, "student": student, "user": user})


def add_course(request, pk, pk2):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, pk=pk2)
    student.courses.add(course)
    student.save()

    user = get_object_or_404(User, pk=pk2)
    return render(request, 'student_dash.html', {"user": user})


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
