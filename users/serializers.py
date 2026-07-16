from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, StudentProfile, CompanyProfile, SupervisorProfile


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'role']

        # Check if all passwords match
        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Passwords didn't match, make sure you are entering same correct password twice."})
            return attrs
        
        def create(self, validated_data):
            validated_data.pop('password2')
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password'],
                role=validated_data['role']
            )

            return user
        
# Student Profile Serializer
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['user', 'full_name', 'tvetstudent_id', 'course_area', 'school_name']

# Company Profile Serializer
class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['user', 'company_representative_name', 'company_name', 'company_sector', 'rdb_registration_number', 'company_address']

# Supervisor Profile Serializer
class SupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorProfile
        fields = ['user', 'full_name', 'school_name', 'department']