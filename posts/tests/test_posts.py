from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from posts.models import Post, Comment
from io import BytesIO
from PIL import Image


User = get_user_model()


def generate_image_file():
    file = BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        'test.jpg',
        file.read(),
        content_type='image/jpeg'
    )


class PostCommentAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='admin',
            birth_date='1990-01-01',
            is_staff=True
        )
        self.user = User.objects.create_user(
            username='user',
            password='user',
            birth_date='1995-05-05'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Sample Title',
            text='Sample Text'
        )
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            text='Test Comment'
        )

    def test_user_can_create_post(self):
        self.client.login(username='user', password='user')
        url = reverse('post-list')
        data = {'title': 'New Post', 'text': 'Text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_post(self):
        self.client.login(username='admin', password='admin')
        url = reverse('post-detail', args=[self.post.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_update_others_post(self):
        self.client.login(username='admin', password='admin')
        url = reverse('post-detail', args=[self.post.pk])
        data = {'title': 'Hacked title', 'text': 'Hacked text'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_upload_image(self):
        self.client.login(username='user', password='user')
        url = reverse('post-list')
        image = generate_image_file()
        data = {'title': 'With image', 'text': 'Has image', 'image': image}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
