import pytest
from datetime import date
from django.core.exceptions import ValidationError

from posts.validators import (
    validate_user_age,
    validate_email,
    validate_post_title,
    validate_password
)


def test_validate_user_age_valid():
    validate_user_age(date(2000, 1, 1))  # возраст > 18 лет, должно пройти


def test_validate_user_age_invalid():
    with pytest.raises(ValidationError):
        validate_user_age(date(2020, 1, 1))  # возраст < 18 лет, ошибка


def test_validate_email_valid():
    validate_email('user@mail.ru')  # разрешённый домен


def test_validate_email_invalid():
    with pytest.raises(ValidationError):
        validate_email('user@gmail.com')  # запрещённый домен


def test_validate_post_title_valid():
    title = 'Это нормальный заголовок'
    validate_post_title(title)  # нет запрещённых слов


def test_validate_post_title_with_forbidden_word():
    title = 'Это какая-то ерунда!'  # содержит запрещённое слово
    with pytest.raises(ValidationError):
        validate_post_title(title)


def test_validate_password_too_short():
    with pytest.raises(ValidationError):
        validate_password('abc12')  # < 8 символов


def test_validate_password_no_digit():
    with pytest.raises(ValidationError):
        validate_password('abcdefgh')  # нет цифр


def test_validate_password_valid():
    validate_password('abc12345')  # валидный пароль
