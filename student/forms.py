from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student

class StudentLoginForm(AuthenticationForm):
    student_id = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Student 
        fields = ['student_id', 'password']

