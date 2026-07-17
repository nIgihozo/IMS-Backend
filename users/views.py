from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import StudentProfile, CompanyProfile, SupervisorProfile
from .serializers import UserSerializer, RegisterSerializer, StudentProfileSerializer, CompanyProfileSerializer, SupervisorProfileSerializer

# Generate JWT token for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# User Registration View
class RegisterView(APIView):
    @extend_schema(request=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({
                'message': 'User Account Created Successfully',
                'user': UserSerializer(user).data,
                'token': token
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class LoginView(APIView):
    @extend_schema(request=UserSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid email or password, Try again!'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = get_tokens_for_user(user)
        return Response(
            {
                'message': 'Logged in successfully',
                'user': UserSerializer(user).data,
                'token': token
            }, status=status.HTTP_200_OK
        )
    
# Student Profile View 
class StudentProfileView(APIView):
    @extend_schema(request=StudentProfileSerializer)
    def post(self, request):
        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
# School Supervisor Profile View
class SupervisorProfileView(APIView):
    @extend_schema(request=SupervisorProfileSerializer)
    def post(self, request):
        serializer = SupervisorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            profile = SupervisorProfile.objects.get(user=request.user)
            serializer = SupervisorProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SupervisorProfile.DoesNotExist:
            return Response({'error': 'Supervisor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
# Company Profile View
class CompanyProfileView(APIView):
    @extend_schema(request=CompanyProfileSerializer)
    def post(self, request):
        serializer = CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            profile = CompanyProfile.objects.get(user=request.user)
            serializer = CompanyProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompanyProfile.DoesNotExist:
            return Response({'error': 'Company profile not found.'}, status=status.HTTP_404_NOT_FOUND)