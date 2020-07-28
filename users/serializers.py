from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "Unable to log in with provided credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Profile Serializer contains total and monthly data

class CreateProfileSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Profile
        fields = ("initial_amount", "total_amount",
                  "total_amount_gained", "total_amount_spent", "monthly_data")

    def create(self, validated_data):
        now = datetime.now()
        monthYear = '{}{}'.format(now.month, now.year)
        print(monthYear)
        instance = Profile.objects.update_or_create(user=self.context['request'].user,
                                                    initial_amount=validated_data['initial_amount'],
                                                    total_amount=validated_data['total_amount'],
                                                    total_amount_gained=validated_data['total_amount_gained'],
                                                    total_amount_spent=validated_data['total_amount_spent'],
                                                    monthly_data={
                                                        monthYear: {
                                                            "monthly_gained": 0.0,
                                                            "monthly_spent": 0.0
                                                        }
        })
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
