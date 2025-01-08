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


def class_project_code(request):
    """Render the class_project_code.html template."""
    # Define the Python code as a multi-line string
    python_code = """
import csv
import os

# File name for storing student data
FILE_NAME = 'student.csv'

# List to store student records
students = []

def load_data():
    \"\"\"Load student data from the CSV file into the students list.\"\"\"
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert Score to integer for proper sorting
                row['Score'] = int(row['Score'])
                students.append(row)

def save_data():
    \"\"\"Save student data from the students list into the CSV file.\"\"\"
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Major', 'ID', 'Name', 'Gender', 'Subject', 'Score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow(student)

def display_menu():
    \"\"\"Display the main menu.\"\"\"
    print("\\n****************************************")
    print("1. CREATE NEW")
    print("2. SHOW ALL")
    print("3. QUERY")
    print("0. SAVE AND QUIT")
    print("****************************************")

def create_new_student():
    \"\"\"Create a new student record.\"\"\"
    while True:
        print("\\nCreate a new student: Please input the aspects of the student by turn:")
        major = input("Major: ").strip()
        student_id = input("ID: ").strip()
        name = input("Name: ").strip()
        gender = input("Gender: ").strip()
        subject = input("Subject: ").strip()
        while True:
            score_input = input("Score: ").strip()
            if score_input.isdigit():
                score = int(score_input)
                break
            else:
                print("Invalid score. Please enter a numeric value.")
        
        # Check for duplicate ID
        if any(s['ID'] == student_id for s in students):
            print("A student with this ID already exists. Please try again.")
            continue

        student = {
            'Major': major,
            'ID': student_id,
            'Name': name,
            'Gender': gender,
            'Subject': subject,
            'Score': score
        }
        students.append(student)
        print("Student info successfully created.")
        
        cont = input("Would you hope to continue to create a new one? Y/N: ").strip().upper()
        if cont != 'Y':
            break

def merge_sort(data, key, reverse=False):
    \"\"\"Merge Sort algorithm for sorting student records.\"\"\"
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key, reverse)
    right = merge_sort(data[mid:], key, reverse)
    return merge(left, right, key, reverse)

def merge(left, right, key, reverse):
    \"\"\"Helper function for merge sort.\"\"\"
    merged = []
    while left and right:
        if reverse:
            condition = left[0][key] > right[0][key]
        else:
            condition = left[0][key] < right[0][key]
        if condition:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
    merged.extend(left if left else right)
    return merged

def quick_sort(data, key, reverse=False):
    \"\"\"Quick Sort algorithm for sorting student records.\"\"\"
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2][key]
    left = []
    middle = []
    right = []
    for student in data:
        if student[key] < pivot:
            left.append(student)
        elif student[key] > pivot:
            right.append(student)
        else:
            middle.append(student)
    if reverse:
        return quick_sort(right, key, reverse) + middle + quick_sort(left, key, reverse)
    else:
        return quick_sort(left, key, reverse) + middle + quick_sort(right, key, reverse)

def show_all_students():
    \"\"\"Display all student records with sorting options.\"\"\"
    if not students:
        print("\\nNo student records available.")
        return
    print("\\nMajor\\tID\\tName\\tGender\\tSubject\\tScore")
    for student in students:
        print(f"{student['Major']}\\t{student['ID']}\\t{student['Name']}\\t{student['Gender']}\\t{student['Subject']}\\t{student['Score']}")
    
    while True:
        print("\\nPlease choose the mode for display:")
        print("1. Sort by ID; 2. Sort by Score")
        choice = input("Enter your choice (1/2): ").strip()
        if choice not in ['1', '2']:
            print("Invalid choice. Please enter 1 or 2.")
            continue
        key = 'ID' if choice == '1' else 'Score'
        break
    
    while True:
        print("\\nChoose sorting algorithm:")
        print("1. Merge Sort")
        print("2. Quick Sort")
        algo = input("Enter your choice (1/2): ").strip()
        if algo not in ['1', '2']:
            print("Invalid choice. Please enter 1 or 2.")
            continue
        break
    
    reverse = False
    if key == 'Score':
        while True:
            direction = input("Choose direction: 1. Ascending; 2. Descending: ").strip()
            if direction == '1':
                reverse = False
                break
            elif direction == '2':
                reverse = True
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    # Sorting
    if algo == '1':
        sorted_students = merge_sort(students.copy(), key, reverse)
        algo_name = "Merge Sort (O(n log n))"
    else:
        sorted_students = quick_sort(students.copy(), key, reverse)
        algo_name = "Quick Sort (Average O(n log n), Worst O(n²))"
    
    print(f"\\nStudents sorted by {key} using {algo_name}:")
    print("Major\\tID\\tName\\tGender\\tSubject\\tScore")
    for student in sorted_students:
        print(f"{student['Major']}\\t{student['ID']}\\t{student['Name']}\\t{student['Gender']}\\t{student['Subject']}\\t{student['Score']}")

def query_student():
    \"\"\"Query a student by name and perform modify or delete operations.\"\"\"
    if not students:
        print("\\nNo student records available.")
        return
    name = input("\\nPlease input the student name for query: ").strip()
    matched_students = [s for s in students if s['Name'].lower() == name.lower()]
    if not matched_students:
        print(f"No student found with name '{name}'.")
        return
    for student in matched_students:
        print("\\nMajor\\tID\\tName\\tGender\\tSubject\\tScore")
        print(f"{student['Major']}\\t{student['ID']}\\t{student['Name']}\\t{student['Gender']}\\t{student['Subject']}\\t{student['Score']}")
        while True:
            print("\\nPlease choose the operation on this student:")
            print("1. Modify; 2. Delete; 0. Back to the menu")
            operation = input("Enter your choice (1/2/0): ").strip()
            if operation == '1':
                modify_student(student)
                break
            elif operation == '2':
                delete_student(student)
                break
            elif operation == '0':
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 0.")

def modify_student(student):
    \"\"\"Modify the attributes of a student.\"\"\"
    print(f"\\nTo modify the info of {student['Name']}, please input the items to be modified;")
    print("If you wish to keep the current item without modification, please press Enter.")
    new_major = input(f"Input the new value for attribute 'Major' (current: {student['Major']}): ").strip()
    new_id = input(f"Input the new value for attribute 'ID' (current: {student['ID']}): ").strip()
    new_name = input(f"Input the new value for attribute 'Name' (current: {student['Name']}): ").strip()
    new_gender = input(f"Input the new value for attribute 'Gender' (current: {student['Gender']}): ").strip()
    new_subject = input(f"Input the new value for attribute 'Subject' (current: {student['Subject']}): ").strip()
    while True:
        new_score_input = input(f"Input the new value for attribute 'Score' (current: {student['Score']}): ").strip()
        if new_score_input == '':
            new_score = student['Score']
            break
        elif new_score_input.isdigit():
            new_score = int(new_score_input)
            break
        else:
            print("Invalid score. Please enter a numeric value or press Enter to keep current.")
    
    # Update fields if new values are provided
    if new_major:
        student['Major'] = new_major
    if new_id:
        # Check for duplicate ID
        if any(s['ID'] == new_id and s != student for s in students):
            print("A student with this ID already exists. ID not modified.")
        else:
            student['ID'] = new_id
    if new_name:
        student['Name'] = new_name
    if new_gender:
        student['Gender'] = new_gender
    if new_subject:
        student['Subject'] = new_subject
    student['Score'] = new_score
    print("Modification is successful!")
    print("\\nMajor\\tID\\tName\\tGender\\tSubject\\tScore")
    print(f"{student['Major']}\\t{student['ID']}\\t{student['Name']}\\t{student['Gender']}\\t{student['Subject']}\\t{student['Score']}")

def delete_student(student):
    \"\"\"Delete a student record.\"\"\"
    confirmation = input(f"Are you sure you want to delete the record of {student['Name']}? (Y/N): ").strip().upper()
    if confirmation == 'Y':
        students.remove(student)
        print(f"Student '{student['Name']}' has been deleted.")
    else:
        print("Deletion cancelled.")

def quit_and_save():
    \"\"\"Save data and quit the program.\"\"\"
    save_data()
    print("\\nFile successfully saved. Welcome next use!")
    exit()

def main():
    \"\"\"Main function to run the Student Transcript Management System.\"\"\"
    load_data()
    print("Welcome to the Student Transcript Management System!")
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            create_new_student()
        elif choice == '2':
            show_all_students()
        elif choice == '3':
            query_student()
        elif choice == '0':
            quit_and_save()
        else:
            print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()
"""

    context = {
        'python_code': python_code.strip()
    }
    return render(request, 'students/class_project_code.html', context)

