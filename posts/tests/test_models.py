from django.test import TestCase
from posts.models import User, Post, Comment


class ModelStrTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            birth_date='2000-01-01',
            phone='+79991112233'
        )
        self.post = Post.objects.create(
            title='Title',
            text='Text',
            author=self.user
        )
        self.comment = Comment.objects.create(
            text='Text',
            author=self.user,
            post=self.post
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Пост "Title" от testuser')

    def test_comment_str(self):
        expected = f'Комментарий {self.user} к посту "{self.post}"'
        self.assertEqual(str(self.comment), expected)
