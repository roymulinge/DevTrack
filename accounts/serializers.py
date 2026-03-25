from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'password2')

    def validate_email(self, value):
      
        blocked = ['test.com', 'fake.com', 'example.com', 'mailinator.com', 'tempmail.com']
        domain  = value.split('@')[-1].lower()
        if domain in blocked:
            raise serializers.ValidationError("Please use a real email address.")
        return value.lower()    

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 =serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['newpassword2']:
            raise serializers.ValidationError({"new_password": "New password do not match."})
        return attrs