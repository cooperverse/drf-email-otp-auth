from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class RegisterSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','email', 'password1', 'password2']
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password do not match")
        return data
    
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
            
class Loginserializer(serializers.Serializer):
    email =serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            user = authenticate(email= data['email'], password = data['password']) 
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        
        data['user'] = user
        return data
        