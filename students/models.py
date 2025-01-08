# students/models.py
from django.db import models

class Student(models.Model):
    MAJOR_CHOICES = [
    ('CST', 'Computer Science and Technology'),
    ('SE', 'Software Engineering'),
    ('IT', 'Information Technology'),
    ('ECE', 'Electronics and Communication Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('EE', 'Electrical Engineering'),
    ('CE', 'Civil Engineering'),
    ('AE', 'Aerospace Engineering'),
    ('BME', 'Biomedical Engineering'),
    ('CHE', 'Chemical Engineering'),
    ('ENV', 'Environmental Engineering'),
    ('DS', 'Data Science'),
    ('AI', 'Artificial Intelligence'),
    ('CY', 'Cybersecurity'),
    ('IS', 'Information Systems'),
    ('BT', 'Biotechnology'),
    ('PH', 'Physics'),
    ('CH', 'Chemistry'),
    ('MA', 'Mathematics'),
    ('ECO', 'Economics'),
]


    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    major = models.CharField(max_length=50, choices=MAJOR_CHOICES)
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    subject = models.CharField(max_length=100)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.student_id})"
