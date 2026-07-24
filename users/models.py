from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        SUPERVISOR = 'SUPERVISOR', 'School Supervisor'
        COMPANY = 'COMPANY', 'Company'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
            return f"{self.email} ({self.role})"
        
class StudentProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
        full_name = models.CharField(max_length=255)
        tvetstudent_id = models.CharField(max_length=100, unique=True)
        course_area = models.CharField(max_length=100)
        level = models.CharField(max_length=50)
        school_name = models.CharField(max_length=255)

        def __str__(self):
            return f"{self.full_name} ({self.tvetstudent_id})"
        
class CompanyProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
        company_representative_name = models.CharField(max_length=255)
        representative_role = models.CharField(max_length=150)
        company_name = models.CharField(max_length=255)
        company_sector = models.CharField(max_length=100)
        rdb_registration_number = models.CharField(max_length=100, unique=True)
        company_address = models.TextField()

        def __str__(self):
            return f"{self.company_representative_name} ({self.company_name})"
        
class SupervisorProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_profile')
        full_name = models.CharField(max_length=255)
        school_name = models.CharField(max_length=255)
        department = models.CharField(max_length=100)

        def __str__(self):
            return f"{self.full_name} ({self.school_name})"
        
class PasswordResetToken(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      token = models.UUIDField(default=uuid.uuid4, unique=True)
      created_at = models.DateTimeField(auto_now_add=True)

      def is_valid(self):
            return timezone.now() < self.created_at + timedelta(minutes=15)
