from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post, Comment
from posts.permissions import IsAdminOrAuthorOrReadOnly

User = get_user_model()


class ViewTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', password='admin', birth_date='1990-01-01'
        )
        self.user = User.objects.create_user(
            username='user', password='user', birth_date='2000-01-01'
        )
        self.other = User.objects.create_user(
            username='other', password='other', birth_date='2000-01-01'
        )
        self.post = Post.objects.create(
            author=self.user, title='Title', text='Text'
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, text='Comment'
        )

    def test_read_post_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_auth_required(self):
        url = reverse('post-list')
        data = {'title': 'T', 'text': 'T'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_by_author(self):
        self.client.force_authenticate(self.user)
        url = reverse('post-detail', args=[self.post.id])
        data = {'title': 'New', 'text': 'Updated'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post_by_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_list_public(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_by_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-list')
        data = {'text': 'New', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment_by_author(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        data = {'text': 'Edited'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_by_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user_allowed_for_anonymous(self):
        url = reverse('user-list')
        data = {
            'username': 'anon',
            'password': 'pass1234',
            'email': 'anon@mail.ru',
            'birth_date': '2000-01-01',
            'phone': '+79990001122'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_anonymous_denied(self):
        url = reverse('comment-list')
        data = {'text': 'Blocked', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_works(self):
        from posts.serializers import UserSerializer
        data = {
            'username': 'created',
            'password': 'pass1234',
            'email': 'user@mail.ru',
            'birth_date': '2000-01-01',
            'phone': '+79991112233'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'created')

    def test_comment_get_permissions_list_action(self):
        from posts.views import CommentViewSet
        view = CommentViewSet()
        view.action = 'list'
        perms = view.get_permissions()
        self.assertEqual(len(perms), 1)
        self.assertTrue(perms[0].__class__.__name__, 'AllowAny')

    def test_post_get_permissions_list_action(self):
        from posts.views import PostViewSet
        view = PostViewSet()
        view.action = 'list'
        perms = view.get_permissions()
        self.assertEqual(len(perms), 1)
        self.assertEqual(perms[0].__class__.__name__, 'AllowAny')

    def test_post_get_permissions_non_list(self):
        from posts.views import PostViewSet
        view = PostViewSet()
        view.action = 'retrieve'
        perms = view.get_permissions()
        self.assertEqual(
            perms[0].__class__.__name__, 'IsAdminOrAuthorOrReadOnly'
        )

    def test_user_get_permissions_non_create(self):
        from posts.views import UserViewSet
        view = UserViewSet()
        view.action = 'retrieve'
        perms = view.get_permissions()
        self.assertEqual(
            perms[0].__class__.__name__, 'IsAdminOrSelfOrReadOnly'
        )

    def test_user_get_permissions_non_create_action(self):
        from posts.views import UserViewSet
        view = UserViewSet()
        view.action = 'retrieve'
        perms = view.get_permissions()
        self.assertEqual(
            perms[0].__class__.__name__, 'IsAdminOrSelfOrReadOnly'
        )

    def test_create_user_via_viewset(self):
        url = reverse('user-list')
        data = {
            'username': 'createdview',
            'password': 'pass1234',
            'email': 'view@mail.ru',
            'birth_date': '2000-01-01',
            'phone': '+79991110000'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_comment_viewset_get_permissions_non_create(self):
        from posts.views import CommentViewSet
        view = CommentViewSet()
        view.action = 'retrieve'
        perms = view.get_permissions()
        self.assertIsInstance(perms[0], IsAdminOrAuthorOrReadOnly)
