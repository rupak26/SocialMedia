from rest_framework import routers, serializers, viewsets



class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    
class VerifyRegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
        
class UserForgetPassword(serializers.Serializer):
    email = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

