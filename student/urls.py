from django.urls import path
from . import views  
from .views import LogoutView, StudentSignupView

app_name = 'student'  

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('signup/', StudentSignupView.as_view(), name='signup'),
]


