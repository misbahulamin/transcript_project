# Generated by Django 5.1.4 on 2025-01-08 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(choices=[('CST', 'Computer Science and Technology'), ('SE', 'Software Engineering'), ('IT', 'Information Technology'), ('ECE', 'Electronics and Communication Engineering'), ('ME', 'Mechanical Engineering'), ('EE', 'Electrical Engineering'), ('CE', 'Civil Engineering'), ('AE', 'Aerospace Engineering'), ('BME', 'Biomedical Engineering'), ('CHE', 'Chemical Engineering'), ('ENV', 'Environmental Engineering'), ('DS', 'Data Science'), ('AI', 'Artificial Intelligence'), ('CY', 'Cybersecurity'), ('IS', 'Information Systems'), ('BT', 'Biotechnology'), ('PH', 'Physics'), ('CH', 'Chemistry'), ('MA', 'Mathematics'), ('ECO', 'Economics')], max_length=50)),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('subject', models.CharField(max_length=100)),
                ('score', models.PositiveIntegerField()),
            ],
        ),
    ]
