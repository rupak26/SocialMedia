from .models import User
from .serializers import UserRegisterSerializer , VerifyRegisterSerializer , LoginSerializer ,PasswordResetSerializer,UserForgetPassword
from django.contrib.auth import authenticate
from django.contrib.auth import logout
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
        try: 
            serializer = UserRegisterSerializer(data = request.data)
            if serializer.is_valid():
                validated_data = dict(serializer.data)
                if User.objects.filter(email=validated_data['email']).exists():
                    return Response({'msg' : 'User Alredy Exists'},status=status.HTTP_207_MULTI_STATUS)
                else:
                    user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
                    user.save()
                    send_otp_via_mail(validated_data['email'])
                    return Response({'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class VerifyRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            serializer = VerifyRegisterSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = User.objects.filter(email=email).first()
                if not user:
                    return Response({
                        'msg' : 'Email Does not exist'
                    },status=status.HTTP_404_NOT_FOUND)
                if not user.otp == otp:
                    return Response({
                        'msg' : 'Provided Otp Does not Match'
                    },status=status.HTTP_403_FORBIDDEN)
                
                user.is_verified = True
                user.save()
                return Response({
                       'msg' : 'Account Verified'
                })
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                validated_date = dict(serializer.data)
                user = authenticate(email = validated_date["email"], password = validated_date["password"])
                if user:
                    desire_id  = user.id
                    return Response({"token" : get_tokens_for_user(user)})
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg' : 'Logout Succesfully'},status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ForgetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserForgetPassword(data = request.data)
            if serializer.is_valid():
                validated_data = dict(serializer.data)
                email = validated_data['email']
                user = User.objects.filter(email=email).first()
                if user.is_verified == True:
                    send_otp_via_mail(email)
                    return Response({
                        'msg' : 'new otp sent'
                    },status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({
                        'msg' : 'User is not verified'
                    },status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    serializer._errors
                },status=status.HTTP_409_CONFLICT)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserPasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = PasswordResetSerializer(data = request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                new_password = serializer.data['new_password']
                user = User.objects.filter(email=email).first()
                if not user:
                    return Response({
                        'msg' : 'Email Does not exist in Database'
                    },status=status.HTTP_404_NOT_FOUND)
                if not user.otp == otp:
                    return Response({
                        'msg' : 'Provided Otp Does not Match'
                    },status=status.HTTP_403_FORBIDDEN)
                user.set_password(new_password)
                user.save()
                return Response({
                    'msg' : 'Password Reset Successfully'
                },status=status.HTTP_202_ACCEPTED)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        