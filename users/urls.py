from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentRegisterView, CompanyRegisterView, SupervisorRegisterView, LoginView, ForgotPasswordView, ResetPasswordView

# Auth URLs Endpoints

urlpatterns = [
    path('register/student/', StudentRegisterView.as_view(), name='register-student'),
    path('register/company/', CompanyRegisterView.as_view(), name='register-company'),
    path('register/supervisor/', SupervisorRegisterView.as_view(), name='register-supervisor'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password')
    
]


