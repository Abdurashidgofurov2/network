from rest_framework import serializers
from .models import User
from drf_extra_fields.fields import Base64ImageField


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(write_only=False, default=False, required=False)
    avatar = Base64ImageField(allow_null=True, required=False)  # Ensure this field is correct

    class Meta:
        model = User
        fields = [
            'username', 'last_name', 'family_name', 'email', 'password',
            'confirm_password', 'is_admin', 'avatar', 'old', 'sex', 'bio'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'last_name', 'family_name', 'email', 'avatar', 'old', 'sex', 'bio'
        ]
        read_only_fields = ['phone_number']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)
        instance.email = validated_data.get('email', instance.email)
        instance.old = validated_data.get('old', instance.old)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.bio = validated_data.get('bio', instance.bio)
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        elif not instance.avatar:
            instance.avatar = 'account/avatar/avatar.jpg'
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'username', 'last_name', 'family_name', 'email',
            'avatar', 'old', 'sex', 'bio', 'posts', 'followers', 'join_date', 'followers',
            'avatar_thumbnail', 'back_image'

        ]


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()

