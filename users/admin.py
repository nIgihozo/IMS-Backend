from django.contrib import admin
from .models import User, StudentProfile, SupervisorProfile, CompanyProfile

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(SupervisorProfile)
admin.site.register(CompanyProfile)
