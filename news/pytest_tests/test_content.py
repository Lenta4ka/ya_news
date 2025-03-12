import pytest

from django.urls import reverse
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, news_list):
    # Подсчет постов на главной странице
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


def test_form_for_anonim_and_login(
        news, author_client):
    # Отображение формы на страницах редактирования и удаления
    # для зарегистрированного пользователя.
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert ('form' in response.context)
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_form_for_anonim_and_login(
        news, client):
    # Отображение формы на страницах редактирования и удаления
    # для анонимного пользователя.
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert ('form' in response.context) is False


@pytest.mark.django_db
def test_order_news_list(news_list, client):
    # Проверка сортировки новостей на главной странице
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['object_list']
    all_date_in_news = [obj_news.date for obj_news in news_list]
    sorted_dates = sorted(all_date_in_news, reverse=True)
    assert all_date_in_news == sorted_dates


@pytest.mark.django_db
def test_order_comment(news, client, comments):
    # Проверка сортировки комментарией на отдельной странице новости
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    all_comments = news.comment_set.all()
    all_date_in_comments = [comment.created for comment in all_comments]
    sorted_dates = sorted(all_date_in_comments)
    assert all_date_in_comments == sorted_dates
