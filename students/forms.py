# students/forms.py
from django import forms
from .models import Student
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['major', 'student_id', 'name', 'gender', 'subject', 'score']
        widgets = {
            'major': forms.Select(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
