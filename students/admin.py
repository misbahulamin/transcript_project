# students/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'major', 'gender', 'subject', 'score')
    search_fields = ('student_id', 'name')
    list_filter = ('major', 'gender')
