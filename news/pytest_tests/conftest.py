# conftest.py
from datetime import datetime, timedelta
from django.utils import timezone
import pytest

# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news(author):
    today = timezone.now()
    news = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        date=today,
        text='Текст заметки',
    )
    return news

@pytest.fixture
def comment(news,author):
    today = timezone.now()
    comment = Comment.objects.create(
        news = news,
        created  = today,
        text = 'комментарий из фикстур',
        author = author,)
    return comment

@pytest.fixture
def comments(news,author):
    today = timezone.now()
    comments = []
    for index in range(5):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}',
            created=today - timedelta(days=index),
        )
        comment.save()
        comments.append(comment)
    return comments
@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def id_for_args(news):  
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.id,)

@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def id_comment_for_args(comment):  
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (comment.id,)

@pytest.fixture
def news_list():
    today = timezone.now()
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News.objects.create(
            title=f'Новость {index}',
            date=today - timedelta(days=index),
            text='Просто текст.')
        news.save()
    return index

@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }