# students/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator
from django.db.models import Q
import csv
from django.http import HttpResponse

def home(request):
    """Home view displaying the welcome message and menu."""
    return render(request, 'students/home.html')

def create_student(request):
    """View to create a new student."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student info successfully created.')
            if 'add_another' in request.POST:
                return redirect('students:create_student')
            else:
                return redirect('students:home')
    else:
        form = StudentForm()
    return render(request, 'students/create_student.html', {'form': form})

def list_students(request):
    """View to list all students with sorting options."""
    sort_by = request.GET.get('sort', 'student_id')
    order = request.GET.get('order', 'asc')
    if sort_by not in ['student_id', 'score']:
        sort_by = 'student_id'
    if order == 'desc':
        sort_by = '-' + sort_by
    students = Student.objects.all().order_by(sort_by)

    # Pagination (optional)
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/list_students.html', {'page_obj': page_obj, 'sort': sort_by.strip('-'), 'order': order})

def query_student(request):
    """View to query students by name."""
    query = request.GET.get('q')
    results = []
    if query:
        results = Student.objects.filter(name__icontains=query)
    return render(request, 'students/query_student.html', {'results': results, 'query': query})

def modify_student(request, pk):
    """View to modify a student's information."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification is successful!')
            return redirect('students:list_students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/modify_student.html', {'form': form, 'student': student})

def delete_student(request, pk):
    """View to delete a student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f"Student '{student.name}' has been deleted.")
        return redirect('students:list_students')
    return render(request, 'students/delete_student.html', {'student': student})

def export_csv(request):
    """View to export all student data to CSV."""
    students = Student.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student.csv"'

    writer = csv.writer(response)
    writer.writerow(['Major', 'ID', 'Name', 'Gender', 'Subject', 'Score'])
    for student in students:
        writer.writerow([student.major, student.student_id, student.name, student.gender, student.subject, student.score])

    return response
