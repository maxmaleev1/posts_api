from django.contrib import admin
from rangefilter.filters import DateRangeFilter  # календарный фильтр
from .models import User, Post, Comment
from django.utils.html import format_html
from django.urls import reverse


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'birth_date')
    search_fields = ('username', 'email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author_link', 'created_at')
    list_filter = (('created_at', DateRangeFilter),)

    def author_link(self, obj):
        url = reverse('admin:posts_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)

    author_link.short_description = 'Автор'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    list_filter = (('created_at', DateRangeFilter),)  # календарный фильтр
