from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, StudentProfileView, CompanyProfileView, SupervisorProfileView

# Auth URLs Endpoints

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile URLs Endpoints
    path('profile/student/', StudentProfileView.as_view(), name='student-profile'),
    path('profile/company/', CompanyProfileView.as_view(), name='company-profile'),
    path('profile/supervisor/', SupervisorProfileView.as_view(), name='supervisor-profile'),
]


