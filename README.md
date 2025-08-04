# 📘 Проект: API для постов и комментариев

## 📦 Описание

Django-проект с REST API, реализующий взаимодействие пользователей, постов и комментариев. Поддерживается регистрация, JWT-аутентификация, а также разграничение прав доступа по ролям.

## 🚀 Технологии

- Python 3.10
- Django 3.2
- Django REST Framework
- Simple JWT
- PostgreSQL
- Docker + Docker Compose
- drf-spectacular (автодокументация)

## ⚙️ Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/maxmaleev1/posts_api.git
cd posts_api
```

2. Создай `.env` файл на основе `.env.example`:

```bash
cp .env.example .env
```

3. Собери и запусти контейнеры:

```bash
docker compose up -d --build
```

4. Перейди в браузере:

- Приложение: http://127.0.0.1:8000/
- Документация: http://127.0.0.1:8000/schema/swagger/

## 🧪 Тесты и покрытие

```bash
docker compose exec web pytest --cov=.
```

## 👤 Администратор

- **Логин:** admin
- **Пароль:** admin

## 🔗 Эндпоинты:

### Пользователь

```
GET     /posts/users/
POST    /posts/users/
GET     /posts/users/<id>/
PUT     /posts/users/<id>/
PATCH   /posts/users/<id>/
DELETE  /posts/users/<id>/
```

### Пост

```
GET     /posts/posts/
POST    /posts/posts/
GET     /posts/posts/<id>/
PUT     /posts/posts/<id>/
PATCH   /posts/posts/<id>/
DELETE  /posts/posts/<id>/
```

### Комментарий

```
GET     /posts/comments/
POST    /posts/comments/
GET     /posts/comments/<id>/
PUT     /posts/comments/<id>/
PATCH   /posts/comments/<id>/
DELETE  /posts/comments/<id>/
```