from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Кастомная модель пользователя. Логин и пароль уже включены'''
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    '''Модель поста. Связь с комментариями через related_name="comments"'''
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Пост "{self.title}" от {self.author}'


class Comment(models.Model):
    '''Модель комментария (+ связь с постом)'''
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Комментарий {self.author} к посту "{self.post}"'
