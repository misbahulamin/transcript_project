# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_student, name='create_student'),
    path('list/', views.list_students, name='list_students'),
    path('query/', views.query_student, name='query_student'),
    path('modify/<int:pk>/', views.modify_student, name='modify_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('export_csv/', views.export_csv, name='export_csv'),
]
