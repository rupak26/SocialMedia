from rest_framework import routers, serializers, viewsets



class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    
class VerifyRegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField()

class loginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
        
class userForgetPassword(serializers.Serializer):
    email = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

