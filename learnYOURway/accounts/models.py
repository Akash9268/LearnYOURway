from django.db import models
from django.contrib.auth.models import AbstractUser  # default fields = firstname, lastname, isstaff.....
from django.core.validators import MinLengthValidator
from django.utils import timezone
from learning.models import Course


# Create your models here.


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=True)
    email_id = models.EmailField(max_length=100,null=True,blank=True,default=None)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Highest_qualification = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField(null=True, blank=True, validators=[MinLengthValidator(70)])

    def __str__(self):
        return self.user.first_name + self.user.last_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    courses = models.ManyToManyField(Course)
    phone_no = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Order(models.Model):
    payment_status_choice = {
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING')
    }
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    payment_status = models.IntegerField(choices=payment_status_choice, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # RAZORPAY INFO
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


class CourseOrder(models.Model):
    class Meta:
        unique_together = (('order', 'course'),)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.FloatField()
