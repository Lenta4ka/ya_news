import pytest

from django.urls import reverse
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_count(client, news_list):
# Подсчет постов на главной странице
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count is NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db 
@pytest.mark.parametrize(
    'parametrized_client, form_in_page',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True)
    ),
)
def test_form_for_anonim_and_login(
        news, parametrized_client, form_in_page):
    # Отображение формы на страницах редактирования и удаления
    # для зарегистрированного и анонимного пользователей.
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_page

@pytest.mark.django_db 
def test_order_news_list(news_list,client):
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
    url = reverse('news:detail', args =(news.id,))
    response = client.get(url)
    print(response.context)
    assert 'news' in response.context
    '''all_comments = news.comment_set.all()
    all_date_in_comments = [comment.created for comment in all_comments]
    sorted_dates = sorted(all_date_in_comments)
    assert all_date_in_comments == sorted_dates'''
