from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from rest_framework.views  import APIView
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializers, VerifyOTPSerializer, Loginserializer
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .utils import generate_otp, get_token_for_user



class RegisterApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializers(data = request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.create(
                    username=serializer.validated_data['username'],
                    email = serializer.validated_data['email'],
                    password =serializer.validated_data['password1'],
                    is_active = False
                )
                otp = generate_otp()
                user.email_otp = otp
                user.otp_created_at = timezone.now()
                user.save()
                
                send_mail('Verification Code', f"Your OTP is:{otp}",settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
                return Response({
                    'message':"User created. Check your email for the otp.",
                    'email':user.email
                }, status= status.HTTP_201_CREATED)
            
            except:
                return Response({"message":"Give Valid Informaton"})
            
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data = request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = get_object_or_404(CustomUser, email=email)
            
            if user.is_otp_expired():
                new_otp = generate_otp()
                user.email_otp = new_otp
                user.otp_created_at = timezone.now()
                user.save()
                send_mail("New OTP", f"Your new OTP is {new_otp}",settings.EMAIL_HOST_USER, [user.email],fail_silently=True)
                return Response({"message":"You otp expaired. A new OTP has been sent to your mail"}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.otp_cooldown():
                return Response({"message":"Wait for 30 seconds before requesting OTP "}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.email_otp != otp:
                return Response({"message":"Invalid OTP. Please try again."},status=status.HTTP_400_BAD_REQUEST)
            
            if user.email_otp == otp:
                user.is_active = True
                user.is_email_verified = True
                user.otp_created_at = None
                user.email_otp = None
                user.save()
                
                tokens = get_token_for_user(user)
                return Response({
                    "messege":"Email Verified Successfully",
                    "toekn":tokens
                }, status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid OTP. Please try again."},status=status.HTTP_400_BAD_REQUEST)
            
        
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(generics.GenericAPIView):
    serializer_class = Loginserializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = get_object_or_404(CustomUser, email=email)
        if not check_password(password, user.password):
            return Response({"message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        tokens = get_token_for_user(user)
        
        return Response({"messaage":"Login successful","tokens":tokens},status=status.HTTP_200_OK)
        
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message":"Logged out successfully"},status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error":"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserDetailView(generics.RetrieveAPIView):
        
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializers
    
    def get_object(self):
        return self.request.user
            
            