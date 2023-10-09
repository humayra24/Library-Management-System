from django.shortcuts import render,redirect
from .models import Student
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import StudentLoginForm
from django.contrib.auth import login as auth_login


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'Logout successful')
        return redirect('home')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['studentID'], password=request.POST['password'])
        print(user)                        
        if user is None:
            messages.error(request,'Invalid CREDENTIALS')
            return redirect('/student/login/')
        else:
            auth.login(request, user)
            messages.success(request,'Login successful')
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
    else:
        return render(request, 'student/login.html')


class StudentSignupView(View):
    template_name = 'student/signup.html'  

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        studentID = request.POST.get('studentID')
        password = request.POST.get('password')

        if not firstname or not lastname or not studentID or not password:
            messages.error(request, 'All fields must be filled out.')
            return render(request, self.template_name)

        try:
            user = User.objects.get(username=studentID)
            messages.success(request, 'User already exists with the same StudentID!')
            return redirect('/student/login/')
        except User.DoesNotExist:
            user = User.objects.create_user(username=studentID, password=password)

            newstudent = Student.objects.create(
                first_name=firstname,
                last_name=lastname,
                student_id=user
            )
            auth_login(request, user)
            messages.success(request, 'Signup successful')
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')

    def get(self, request):
        return render(request, self.template_name)
