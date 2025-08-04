from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from datetime import date

from posts.serializers import PostSerializer, CommentSerializer, UserSerializer
from posts.models import Post, Comment
from posts.constants import BANNED_TITLE_WORDS


User = get_user_model()


class SerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            birth_date=date(2000, 1, 1),
            email='user@example.com',
            phone='+70001112233'
        )
        self.post = Post.objects.create(
            title='Test Title',
            text='Test text',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Test comment'
        )

    def test_post_serializer_valid(self):
        data = {
            'title': 'New Post',
            'text': 'Some content',
        }
        context = {'request': self.client.request().wsgi_request}
        context['request'].user = self.user
        context['request'].method = 'POST'
        serializer = PostSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_post_serializer_forbidden_word(self):
        data = {
            'title': f'Title with {BANNED_TITLE_WORDS[0]}',
            'text': 'Some content',
        }
        context = {'request': self.client.request().wsgi_request}
        context['request'].user = self.user
        context['request'].method = 'POST'
        serializer = PostSerializer(data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_post_serializer_unauthenticated(self):
        data = {
            'title': 'No Auth',
            'text': 'Test',
        }
        request = self.client.request().wsgi_request
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        request.method = 'POST'
        serializer = PostSerializer(data=data, context={'request': request})
        with self.assertRaises(PermissionDenied):
            serializer.is_valid(raise_exception=True)

    def test_comment_serializer_fields(self):
        serializer = CommentSerializer(instance=self.comment)
        data = serializer.data
        self.assertEqual(set(data.keys()), {
            'id', 'text', 'post', 'author', 'created_at', 'updated_at'
        })

    def test_comment_serializer_validation(self):
        data = {
            'text': '',
            'post': self.post.pk
        }
        serializer = CommentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)

    def test_user_serializer_valid(self):
        data = {
            'username': 'newuser',
            'password': 'pass1234',
            'email': 'user@mail.ru',
            'birth_date': date(2000, 1, 1),
            'phone': '+79998887766'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_user_serializer_invalid_password(self):
        data = {
            'username': 'badpass',
            'password': 'short',
            'email': 'user@mail.ru',
            'birth_date': date(2000, 1, 1),
            'phone': '+79998887766'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_user_serializer_invalid_email(self):
        data = {
            'username': 'badmail',
            'password': 'goodpass123',
            'email': 'user@gmail.com',
            'birth_date': date(2000, 1, 1),
            'phone': '+79998887766'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_comment_serializer_unauthenticated(self):
        data = {'text': 'Nice', 'post': self.post.pk}
        anon = type('AnonymousUser', (), {'is_authenticated': False})()
        request = self.client.request().wsgi_request
        request.user = anon
        request.method = 'POST'
        serializer = CommentSerializer(data=data, context={'request': request})
        with self.assertRaises(PermissionDenied):
            serializer.is_valid(raise_exception=True)

    def test_comment_serializer_admin(self):
        admin = User.objects.create_user(
            username='admin', password='admin', is_staff=True,
            birth_date=date(1980, 1, 1), email='admin@mail.ru',
            phone='+79995556677'
        )
        data = {'text': 'Test', 'post': self.post.pk}
        request = self.client.request().wsgi_request
        request.user = admin
        request.method = 'POST'
        serializer = CommentSerializer(data=data, context={'request': request})
        with self.assertRaises(PermissionDenied):
            serializer.is_valid(raise_exception=True)

    def test_user_serializer_create_all_fields(self):
        data = {
            'username': 'full',
            'password': 'pass1234',
            'email': 'full@mail.ru',
            'birth_date': '2000-01-01',
            'phone': '+79991112233'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, 'full@mail.ru')
        self.assertEqual(user.phone, '+79991112233')

    def test_user_serializer_create_only_required_fields(self):
        data = {
            'username': 'minimal',
            'password': 'pass1234',
            'email': 'user@mail.ru',
            'birth_date': '2000-01-01',
            'phone': '+79998887766'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'minimal')

    def test_user_serializer_invalid_email_validation(self):
        data = {
            'username': 'emailcheck',
            'password': 'pass1234',
            'email': 'invalid@gmail.com',  # запрещённый домен
            'birth_date': '2000-01-01',
            'phone': '+79991112233'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_validate_password_accepts_valid_password(self):
        serializer = UserSerializer()
        valid_password = 'abc12345'
        result = serializer.validate_password(valid_password)
        self.assertEqual(result, valid_password)
