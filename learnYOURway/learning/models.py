from django.db import models

# Create your models here.

class Course(models.Model):
    taught_by = models.ForeignKey(to='accounts.Teacher',on_delete=models.CASCADE)
    Subject_name = models.CharField(max_length=100,blank=False)
    Description = models.TextField(null=True, blank=False)
    Course_fee = models.IntegerField(null=True, blank=False)
    Class_link = models.URLField(max_length=200,null=True)
    Duration = models.CharField(max_length=20,null=True, blank=False)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.Subject_name


