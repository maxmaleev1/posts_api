from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post, Comment
from datetime import datetime, timedelta, time
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей, 15 постов и комментарии'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        User.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()

        admin = User.objects.create_user(
            username='admin',
            email='admin@mail.ru',
            phone='1111111111',
            birth_date=datetime(1990, 1, 1).date(),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        admin.set_password('admin')
        admin.save()

        underage = User.objects.create_user(
            username='underage',
            email='underage@mail.ru',
            phone='2222222222',
            birth_date=datetime(2010, 1, 1).date(),
            is_active=True,
        )
        underage.set_password('admin')
        underage.save()

        adult = User.objects.create_user(
            username='adult',
            email='adult@mail.ru',
            phone='3333333333',
            birth_date=datetime(1995, 1, 1).date(),
            is_active=True,
        )
        adult.set_password('admin')
        adult.save()

        TEST = User.objects.create_user(
            username='TEST',
            email='TEST@mail.ru',
            phone='4444444444',
            birth_date=datetime(2000, 1, 1).date(),
            is_active=True,
        )
        TEST.set_password('admin')
        TEST.save()

        base_date = timezone.now().date() - timedelta(days=14)
        posts = []
        for i in range(15):
            post = Post.objects.create(
                title=f'Пост №{i + 1}',
                text=f'Содержимое поста №{i + 1}',
                author=adult,
            )
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            dt = datetime.combine(
                base_date + timedelta(days=i),
                time(hour=hour, minute=minute, second=second),
            )
            post.created_at = timezone.make_aware(dt)
            post.save(update_fields=['created_at'])
            posts.append(post)

        for post in posts:
            for j in range(2):
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                dt = datetime.combine(
                    post.created_at.date(),
                    time(hour=hour, minute=minute, second=second),
                )
                Comment.objects.create(
                    author=adult,
                    post=post,
                    text=f'Комментарий {j + 1} к посту "{post.title}"',
                    created_at=timezone.make_aware(dt),
                )

        self.stdout.write(self.style.SUCCESS(
            'Созданы пользователи, 15 постов с датами и 30 комментариев'
        ))
