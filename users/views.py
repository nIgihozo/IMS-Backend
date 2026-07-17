from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer, LoginSerializer,
    StudentRegisterSerializer, CompanyRegisterSerializer, SupervisorRegisterSerializer
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class StudentRegisterView(APIView):
    @extend_schema(request=StudentRegisterSerializer)
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Student account created successfully',
                'user': UserSerializer(user).data,
                'token': get_tokens_for_user(user)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyRegisterView(APIView):
    @extend_schema(request=CompanyRegisterSerializer)
    def post(self, request):
        serializer = CompanyRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Company account created successfully',
                'user': UserSerializer(user).data,
                'token': get_tokens_for_user(user)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupervisorRegisterView(APIView):
    @extend_schema(request=SupervisorRegisterSerializer)
    def post(self, request):
        serializer = SupervisorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Supervisor account created successfully',
                'user': UserSerializer(user).data,
                'token': get_tokens_for_user(user)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @extend_schema(request=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Invalid email or password, try again!'},
                             status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'message': 'Logged in successfully',
            'user': UserSerializer(user).data,
            'token': get_tokens_for_user(user)
        }, status=status.HTTP_200_OK)