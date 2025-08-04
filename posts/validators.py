import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .constants import ALLOWED_EMAIL_DOMAINS, BANNED_TITLE_WORDS


def validate_password(password):
    '''
    Пароль должен быть не короче 8 символов и содержать хотя бы одну цифру
    '''
    if len(password) < 8:
        raise ValidationError(_('Пароль должен содержать не менее 8 символов'))
    if not any(char.isdigit() for char in password):
        raise ValidationError(_('Пароль должен содержать хотя бы одну цифру'))


def validate_email(email):
    '''
    Разрешены только домены: mail.ru, yandex.ru (см. ALLOWED_EMAIL_DOMAINS)
    '''
    domain = email.split('@')[-1]
    if domain not in ALLOWED_EMAIL_DOMAINS:
        raise ValidationError(_(f'Недопустимый домен: {domain}'))


def validate_user_age(birth_date):
    '''Автор должен быть не моложе 18 лет'''
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    if age < 18:
        raise ValidationError(_('Автор должен быть старше 18 лет'))


def validate_post_title(title):
    '''
    Заголовок не должен содержать запрещённых слов (см. BANNED_TITLE_WORDS)
    '''
    lower_title = title.lower()
    for word in BANNED_TITLE_WORDS:
        if re.search(rf'\b{re.escape(word)}\b', lower_title):
            raise ValidationError(
                _(f'Заголовок содержит запрещённое слово: "{word}"')
            )
