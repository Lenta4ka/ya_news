# test_routes.py
from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


def test_detal_pages_anonim(client, news):
    url = reverse('news:detail', args =(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit',),
)
def test_pages_availability_for_author(
       name, author_client,comment
):
    url = reverse(name, args=(comment.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK
   

@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit',),
)
def test_pages_availability_for_not_author(
       name, not_author_client,comment
):
    url = reverse(name, args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
   


@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete'
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, comment):#, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)