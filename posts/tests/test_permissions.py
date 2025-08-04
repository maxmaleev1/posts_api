from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.permissions import SAFE_METHODS

from posts.models import User, Post
from posts.permissions import (IsAdminOrAuthorOrReadOnly,
                               IsAdminOrSelfOrReadOnly)


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', password='admin', is_staff=True,
            birth_date='1980-01-01'
        )
        self.author = User.objects.create_user(
            username='author', password='author',
            birth_date='1990-01-01'
        )
        self.other = User.objects.create_user(
            username='other', password='other',
            birth_date='2000-01-01'
        )
        self.post = Post.objects.create(
            title='Test Post', text='Content', author=self.author
        )
        self.factory = APIRequestFactory()

    def test_admin_can_delete_any_post(self):
        request = self.factory.delete('/')
        request.user = self.admin
        perm = IsAdminOrAuthorOrReadOnly()
        self.assertTrue(perm.has_object_permission(request, None, self.post))

    def test_author_can_update_own_post(self):
        request = self.factory.put('/')
        request.user = self.author
        perm = IsAdminOrAuthorOrReadOnly()
        self.assertTrue(perm.has_object_permission(request, None, self.post))

    def test_other_cannot_delete_post(self):
        request = self.factory.delete('/')
        request.user = self.other
        perm = IsAdminOrAuthorOrReadOnly()
        self.assertFalse(perm.has_object_permission(request, None, self.post))

    def test_safe_methods_are_allowed(self):
        for method in SAFE_METHODS:
            request = self.factory.get('/')
            request.method = method
            request.user = self.other
            perm = IsAdminOrAuthorOrReadOnly()
            self.assertTrue(
                perm.has_object_permission(request, None, self.post)
            )


class IsAdminOrSelfOrReadOnlyTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', password='admin', is_staff=True,
            birth_date='1980-01-01'
        )
        self.user = User.objects.create_user(
            username='user', password='user', birth_date='1995-01-01'
        )
        self.other = User.objects.create_user(
            username='other', password='other', birth_date='2000-01-01'
        )
        self.factory = APIRequestFactory()

    def test_post_request_allowed_for_anyone(self):
        request = self.factory.post('/')
        request.user = self.other
        perm = IsAdminOrSelfOrReadOnly()
        self.assertTrue(perm.has_permission(request, None))

    def test_get_request_requires_authentication(self):
        request = self.factory.get('/')
        request.user = self.other
        perm = IsAdminOrSelfOrReadOnly()
        self.assertTrue(perm.has_permission(request, None))

    def test_delete_requires_admin(self):
        request = self.factory.delete('/')
        request.user = self.user
        perm = IsAdminOrSelfOrReadOnly()
        self.assertFalse(perm.has_object_permission(request, None, self.user))

    def test_user_can_access_self(self):
        request = self.factory.get('/')
        request.user = self.user
        perm = IsAdminOrSelfOrReadOnly()
        self.assertTrue(perm.has_object_permission(request, None, self.user))

    def test_admin_can_access_any(self):
        request = self.factory.get('/')
        request.user = self.admin
        perm = IsAdminOrSelfOrReadOnly()
        self.assertTrue(perm.has_object_permission(request, None, self.user))
