from django.db import models

# Create your models here.

TOPIC_CHOICES = (
		('Physics','Physics'),
		('Mathematics','Mathematics'),
		('Chemistry','Chemistry'),
		('Computer Science','Computer Science'),
		('Networking','Networking'),
)

class Course(models.Model):
    taught_by = models.ForeignKey(to='accounts.Teacher',on_delete=models.CASCADE,related_name='courses')
    Subject_name = models.CharField(max_length=100,blank=False)
    Description = models.TextField(null=True, blank=False)
    Course_fee = models.IntegerField(null=True, blank=False)
    Class_link = models.URLField(max_length=200,null=True)
    Duration = models.CharField(max_length=20,null=True, blank=False)
    is_active = models.BooleanField(default=False)
    tag = models.CharField(max_length=100,null=True,blank=False,choices=TOPIC_CHOICES)
    Course_id = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.Subject_name


