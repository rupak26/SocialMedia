from .models import User
from .serializers import UserRegisterSerializer , VerifyRegisterSerializer , loginSerializer ,PasswordResetSerializer,userForgetPassword
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from django.core.mail import send_mail
import random
from django.conf import settings


def send_otp_via_mail(email):
    subject = 'Your email verifications email'
    otp = random.randint(1000,9999)
    message = f'Your Otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject , message , email_from , [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()
  

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            validated_data = dict(serializer.data)
            if User.objects.filter(email=validated_data['email']).exists():
                return Response({'msg' : 'User Alredy Exists'})
            else:
                user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
                user.save()
                send_otp_via_mail(validated_data['email'])
                return Response({'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class VerifyRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = VerifyRegisterSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = User.objects.filter(email=email).first()
            if not user:
               return Response({
                   'msg' : 'Something Went Wrong'
               })
            if not user.otp == otp:
               return Response({
                   'msg' : 'Something Went Wrong'
               })
            
            user.is_verified = True
            user.save()
            return Response({
               'msg' : 'Account Verified'
            })
    

class userLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = loginSerializer(data=request.data)
        if serializer.is_valid():
            validated_date = dict(serializer.data)
            user = authenticate(email = validated_date["email"], password = validated_date["password"])
            if user:
                desire_id  = user.id
                return Response({"token" : get_tokens_for_user(user)})
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ForgetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = userForgetPassword(data = request.data)
        if serializer.is_valid():
            validated_data = dict(serializer.data)
            email = validated_data['email']
            user = User.objects.filter(email=email).first()
            if user.is_verified == True:
               send_otp_via_mail(email)
               return Response({
                  'msg' : 'new otp sent'
               })
            return Response({
               'msg' : 'User is not verified'
            })
        return Response({
            'msg' : 'Somting Went Wrong'
        })

class userPasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            new_password = serializer.data['new_password']
            user = User.objects.filter(email=email).first()
            if not user:
               return Response({
                   'msg' : 'Something Went Wrong'
               })
            if not user.otp == otp:
               return Response({
                   'msg' : 'Something Went Wrong'
               })
            user.set_password(new_password)
            user.save()
            return Response({
               'msg' : 'Password Reset Successfully'
            })
    