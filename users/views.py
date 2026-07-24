from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, PasswordResetToken
from .serializers import (UserSerializer, LoginSerializer,StudentRegisterSerializer, CompanyRegisterSerializer, SupervisorRegisterSerializer, ForgotPasswordSerializer, ResetPasswordSerializer)
from django.core.mail import send_mail
from django.conf import settings


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

class ForgotPasswordView(APIView):
    @extend_schema(request=ForgotPasswordSerializer)
    def post(self, request):
        serializer= ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return Response (
                {'message': 'Reset link for changing password has been sent to your email. Check it out!'},
                status=status.HTTP_200_OK
            )

        reset_token = PasswordResetToken.objects.create(user=user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token.token}"

        send_mail(
            subject='Reset Your IMS Account Password',
            message=f'If you request that you forgot your password, kindly use the link below to reset it. If not please ignore this email and go to your account to take futher step to make your account to be more secure, Thank you!:\n\n{reset_link}\n\nNote: Please note that after 10 minutes this link is going to be expired',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response(
            {'message': 'Reset link for changing password has been sent to your email. Check it out!'},
            status=status.HTTP_200_OK
        )

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    @extend_schema(request=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            reset_obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_obj.is_valid():
            reset_obj.delete()
            return Response({'error': 'This reset link has been expired. Please request a new one!'}, status=status.HTTP_400_BAD_REQUEST)

        
        user = reset_obj.user
        user.set_password(new_password)
        user.save()
        reset_obj.delete()

        return Response(
            {'message': 'Password has been reset successfully. Now you can login!'},
            status=status.HTTP_200_OK
        )
    