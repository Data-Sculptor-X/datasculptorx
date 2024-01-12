# your_app/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.get(username=data['username'])
        if user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            data['refresh_token'] = str(refresh)
            data['access_token'] = str(refresh.access_token)
            data.pop("password")
        else:
            raise serializers.ValidationError("Incorrect credentials")
        return data
