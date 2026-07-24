from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, StudentProfile, CompanyProfile, SupervisorProfile


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']

# Student Registration Serializer
class StudentRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    tvetstudent_id = serializers.CharField()
    course_area = serializers.CharField()
    level = serializers.CharField()
    school_name = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=User.Roles.STUDENT,
            )
            StudentProfile.objects.create(
                user=user,
                full_name=validated_data['full_name'],
                tvetstudent_id=validated_data['tvetstudent_id'],
                course_area=validated_data['course_area'],
                level = validated_data['level'],
                school_name=validated_data['school_name'],
            )
        return user
    
# School Supervisor Registration Serializer
class SupervisorRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    department = serializers.CharField()
    school_name = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=User.Roles.SUPERVISOR,
            )
            SupervisorProfile.objects.create(
                user=user,
                full_name=validated_data['full_name'],
                school_name=validated_data['school_name'],
                department =validated_data['department'],
            )
        return user

# Company Registration Serializer
class CompanyRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    company_representative_name = serializers.CharField()
    representative_role = serializers.CharField()
    company_name = serializers.CharField()
    company_sector = serializers.CharField()
    rdb_registration_number= serializers.CharField()
    company_address = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=User.Roles.COMPANY,
            )
            CompanyProfile.objects.create(
                user=user,
                company_representative_name=validated_data['company_representative_name'],
                representative_role=validated_data['representative_role'],
                company_name=validated_data['company_name'],
                company_sector=validated_data['company_sector'],
                rdb_registration_number=validated_data['rdb_registration_number'],
                company_address=validated_data['company_address'],
            )
        return user
    
# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
        

# Forgot Password Serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email= serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] !=attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs
