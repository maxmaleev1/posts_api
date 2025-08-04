from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

from .models import Post, Comment
from .validators import (
    validate_password,
    validate_email,
    validate_post_title,
    validate_user_age
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для пользователей'''
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone', 'birth_date')

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            birth_date=validated_data.get('birth_date')
        )
        return user


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        validate_post_title(value)
        return value

    def validate(self, data):
        request = self.context['request']
        user = request.user
        if request.method == 'POST':
            if not user.is_authenticated:
                raise PermissionDenied(
                    'Неавторизованный пользователь не может '
                    'создавать посты'
                )
            if user.is_staff:
                raise PermissionDenied(
                    'Администратор не может создавать посты'
                )
            validate_user_age(user.birth_date)
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментариев'''
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context['request']
        user = request.user
        if request.method == 'POST':
            if not user.is_authenticated:
                raise PermissionDenied(
                    'Неавторизованный пользователь не может оставлять '
                    'комментарии'
                )
            if user.is_staff:
                raise PermissionDenied(
                    'Администратор не может оставлять комментарии'
                )
        return data
