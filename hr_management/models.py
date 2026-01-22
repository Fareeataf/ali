from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=7,unique=False)
    description=models.TextField(blank=False)
    create_Date=models.DateField(auto_now_add=True)
 
    def __str__(self):
        return self.name
    

class Designation(models.Model):
    name=models.CharField(max_length=100,unique=True) 
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='designation')
    # create_Date=models.DateField(auto_now_add=True)
    # H_date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
            return self.name

class Employee(models.Model):
     Male='M'
     Female='F'
     choiceGender=[
          (Male,'Male'),
          (Female,'Female'),
     ]
     ID=models.AutoField(primary_key=True)
     first_name=models.CharField(max_length=100)
     last_name=models.CharField(max_length=100)
     middle_name=models.CharField(max_length=100)
     age=models.IntegerField(validators=[MinValueValidator(18),MaxValueValidator(50)])
     email=models.EmailField()
     gender=models.CharField(max_length=1,choices=choiceGender)
     phone=models.CharField(max_length=13,blank=False,null=True)
     profile=models.ImageField(upload_to='profile_picture/',null=True,blank=True) 
     department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
     designation=models.ForeignKey(Designation,on_delete=models.SET_NULL,null=True)
     hire_date=models.DateField(auto_now_add=True,null=True)
     status=models.BooleanField(default=True)
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')

     def __str__(self):
            return f"{self.first_name} {self.last_name}"

class Report(models.Model):
    # allow null for existing reports; form will require selection when creating
    first_name=models.ForeignKey(Employee,on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
