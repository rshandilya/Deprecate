from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICE = (
        ('S', 'student'),
        ('F', 'faculty'),
        ('A', 'admin'),
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICE)

"""
class Contact(models.Model):
    address = models.CharField(max_length=50, blank=True, null=True)
    phone_num1 = models.CharField(max_length=10, blank=True, null=True)
    phone_num2 = models.CharField(max_length=10, blank=True, null=True)
    phone_num3 = models.CharField(max_length=10, blank=True, null=True)
"""


class Student(models.Model):

    BRANCH_CHOICES = (
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('EE', 'EE'),
        ('ME', 'ME'),
        ('CE', 'CE'),
    )
    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
    )
    SEMESTER_CHOICES = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
        (6, 'VI'),
        (7, 'VII'),
        (8, 'VIII'),
    )

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    roll_number = models.CharField(max_length=10, unique=True)
    college_id = models.PositiveSmallIntegerField(unique=True)
    # batch = models.CharField(max_length=4)
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES )
    branch = models.CharField(max_length=3, choices=BRANCH_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, default='A')
    # mother_name = models.CharField(max_length=20, blank=True, null=True)
    # father_name = models.CharField(max_length=20, blank=True, null=True)
    # contact = models.OneToOneField(Contact,
    #                               on_delete=models.CASCADE,
    #                              null=True,
    #                               blank=True)


class Faculty(models.Model):
    DEPT_CHOICES = (
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronic and Communication'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('AS', 'Applied Sciences'),
    )

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    department = models.CharField(max_length=3,choices=DEPT_CHOICES)
    # contact = models.OneToOneField(Contact,
    #                               on_delete=models.CASCADE,
    #                               null=True,
    #                               blank=True)


