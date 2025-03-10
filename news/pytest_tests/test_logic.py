# test_logic.py
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse
from http import HTTPStatus

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_anonymous_user_cant_create_comment(client, form_data, news):
    # Анонимный пользователь не может добавить комментарий
    url = reverse('news:detail', args=(news.id,))
    # Через анонимный клиент пытаемся создать заметку:
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    # Проверяем, что произошла переадресация на страницу логина:
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_login_user_create_comment(author_client, form_data, news):
    # Зарегистрированный пользователь может добавить комментарий
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)
    expected_url = f'{url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']


def test_create_comment_bad_words(author_client, form_data, comment):
    # Комментарий с плохими словами не сохраняется в БД
    url = reverse('news:detail', args=(comment.id,))
    form_data['text'] = BAD_WORDS[0]
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == 1


def test_author_can_delete_comment(author_client, id_for_args):
    # Автор может удалить свой комментарий
    url = reverse('news:delete', args=id_for_args)
    response = author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(
        not_author_client, id_comment_for_args):
    # Не автор удалить комментарий не может
    url = reverse('news:delete', args=id_comment_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, form_data, comment):
    # Автор может редактировать свой комментарий
    url = reverse('news:edit', args=(comment.id,))
    author_client.post(url, form_data)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_note(not_author_client, form_data, comment):
    # Не автор редактировать коммнентарий не может
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
