'''
TODO:
Tests for redirect responses
Tests for disabled shortcuts redirect responses
Tests for non existent shortcuts
Tests for shortcut deletion
Refactor
'''

import string

import pytest

from conftest import test_client
from scr.models.url_shortcut import URLShortcut
from scr.core.config import settings
from .common import validate_keys

SHORTCUT_LETTERS = string.ascii_letters + string.digits


@pytest.mark.parametrize(
    'invalid_url',
    [
        'not_url',
        '',
        None,
        f'{settings.host}/recursive_url'
    ],
)
def test_create_shortcut_invalid_url(invalid_url):
    response = test_client.post(
        '/api/',
        json={'url': invalid_url},
    )
    assert (
        response.status_code == 422
    ), 'Invalid links format or recursive shorcuts must be forbidden'

@pytest.mark.parametrize(
    'status_code', [
        299,
        309,
        301.88,
        'status_code'
    ]
)
def test_create_shortcut_invalid_status_code(status_code):
    response = test_client.post(
        '/api/',
        json={
            'url': 'https://ya.ru/',
            'status_code': status_code
        },
    )
    assert (
        response.status_code == 422
    ), 'Status code of shortcut must be integer 299 < x < 309'


@pytest.mark.parametrize('json', [
    {'id': 100500},
    {'shortcut': 'shortcut'},
    {'disabled': True},
    {'created_at': '2024-01-01T00:00:00'},
    {'updated_at': '2024-01-01T00:00:00'},
    {'shortcut_full': f'{settings.host}/shortcut'},
])
def test_create_shortcut_with_autofilling_fields(json):
    response = test_client.post(
        '/api/',
        json={
            'url': 'https://ya.ru/',
            'status_code': 301,
            **json
        }
    )
    assert (
        response.status_code == 422
    ), 'Autofill fields providing must be forbidden'


def test_get_shortcut(google_shortcut: URLShortcut):
    response = test_client.get('/api/')
    assert (
        response.status_code == 200
    ), 'GET request to `/api/` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), 'GET request to `/api/` endpoint must return `list` object.'
    assert len(response.json()) == 1, (
        'GET request did not return expected objects amount from DB'
    )
    data = response.json()[0]
    validate_keys(data)
    assert response.json() == [
        {
            'created_at': '2024-01-01T00:00:00',
            'updated_at': '2024-01-01T00:00:00',
            'id': google_shortcut.id,
            'url': str(google_shortcut.url),
            'shortcut': str(google_shortcut.shortcut),
            'shortcut_full': f'{settings.host}{google_shortcut.shortcut}',
            'status_code': google_shortcut.status_code,
            'disabled': google_shortcut.disabled,
        }
    ], 'Response from GET request to `/api/` endpoint differs from expected'

def test_get_all_shortcuts(
    google_shortcut: URLShortcut, ya_shortcut: URLShortcut
):
    response = test_client.get('/api/')
    assert (
        response.status_code == 200
    ), 'GET request to `/api/` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), 'GET request to `/api/` endpoint must return `list` object.'
    assert len(response.json()) == 2, (
        'GET request did not return expected objects amount from DB'
    )
    data = response.json()[0]
    validate_keys(data)
    for shortcut in (google_shortcut, ya_shortcut):
        assert (
            {
                'created_at': '2024-01-01T00:00:00',
                'updated_at': '2024-01-01T00:00:00',
                'id': shortcut.id,
                'url': str(shortcut.url),
                'shortcut': str(shortcut.shortcut),
                'shortcut_full': f'{settings.host}{shortcut.shortcut}',
                'status_code': shortcut.status_code,
                'disabled': shortcut.disabled,
            } in response.json()
        ), 'Response from GET request to `/api/` endpoint differs from expected'

@pytest.mark.parametrize('json', [
    {'url': 'https://ya.ru/'},
    {'url': 'https://ya.ru/', 'status_code': 303},
])
def test_create_shortcut(json, freezer):
    freezer.move_to('2024-01-01')
    response = test_client.post(
        '/api/',
        json=json,
    )
    assert (
        response.status_code == 201
    ), 'POST request to `/api/` endpoint must return status code 201.'
    data = response.json()
    validate_keys(data)
    shortcut = data.pop('shortcut')

    for symbol in shortcut:
        assert (
            symbol in SHORTCUT_LETTERS
        ), 'Shortcut must contain only ASCII letters and digits'

    assert data == {
        'url': json['url'],
        'status_code': json['status_code'] if 'status_code' in json else 301,
        'id': 1,
        'created_at': '2024-01-01T00:00:00',
        'updated_at': '2024-01-01T00:00:00',
        'shortcut_full': f'{settings.host}{shortcut}',
        'disabled': False
    }, 'Response from GET request to `/api/` endpoint differs from expected'

@pytest.mark.parametrize('json', [
    {'url': 'not_url'},
    {'status_code': 404},
    {'id': 100500},
    {'shortcut': '_=+^%# @'},
    {'shortcut': 'longname' * 10},
    {'created_at': '2024-01-02T00:00:00'},
    {'updated_at': '2024-01-02T00:00:00'},
    {'shortcut_full': f'{settings.host}shortcut'},
])
def test_update_one_invald_data(google_shortcut: URLShortcut, json):
    response = test_client.patch(
        f'/api/{google_shortcut.shortcut}',
        json=json,
    )
    assert (
        response.status_code == 422
    ), 'Invalid of forbidden data was accepted on update'

def test_update_conflict_shortcut(
    google_shortcut: URLShortcut, ya_shortcut: URLShortcut
):
    response = test_client.patch(
        f'/api/{google_shortcut.shortcut}',
        json={'shortcut': ya_shortcut.shortcut},
    )
    assert (
        response.status_code == 400
    ), 'Shorcuts must be unique'

@pytest.mark.parametrize('json', [
    {'url': 'https://ya.ru/'},
    {'url': 'https://ya.ru/', 'status_code': 303},
    {'url': 'https://ya.ru/', 'shortcut': 'ya2'},
    {'url': 'https://ya.ru/', 'disabled': True},
    {
        'url': 'https://ya.ru/', 
        'disabled': True,
        'shortcut': 'ya2',
        'status_code': 303
    }
])
def test_successfull_update(google_shortcut: URLShortcut, freezer, json):
    update_datetime = '2024-01-02T00:00:00'
    freezer.move_to(update_datetime)
    response = test_client.patch(
        f'/api/{google_shortcut.shortcut}',
        json=json,
    )
    assert (
        response.status_code == 200
    ), 'GET request to `/api/` endpoint must return status code 200.'
    data = response.json()
    validate_keys(data)
    assert data == {
        'url': json['url'],
        'status_code': (
            json['status_code']
            if 'status_code' in json
            else google_shortcut.status_code
        ),
        'id': google_shortcut.id,
        'created_at': '2024-01-01T00:00:00',
        'updated_at': update_datetime,
        'shortcut': (
            json['shortcut'] if 'shortcut' in json
            else str(google_shortcut.shortcut)
        ),
        'shortcut_full': f'{settings.host}{
            json['shortcut'] if 'shortcut' in json
            else str(google_shortcut.shortcut)
        }',
        'disabled': (
            json['disabled'] if 'disabled' in json
            else google_shortcut.disabled
        ),
    }, f'Response from PATCH request to `/api/{google_shortcut.shortcut}` endpoint differs from expected'


def test_disabled_shortcut(disabled_shortcut: URLShortcut):
    response = test_client.get('/api/')
    assert (
        response.status_code == 200
    ), 'GET request to `/api/` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), 'GET request to `/api/` endpoint must return `list` object.'
    assert len(response.json()) == 0, (
        'Disabled shortcuts should not be returned by default'
    )

    response = test_client.get('/api/', params={'include_disabled': True})
    assert (
        response.status_code == 200
    ), 'GET request to `/api/` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), 'GET request to `/api/` endpoint must return `list` object.'
    assert len(response.json()) == 1, (
        'GET request did not return expected objects amount from DB'
    )
    data = response.json()[0]
    validate_keys(data)
    assert response.json() == [
        {
            'created_at': '2024-01-01T00:00:00',
            'updated_at': '2024-01-01T00:00:00',
            'id': disabled_shortcut.id,
            'url': str(disabled_shortcut.url),
            'shortcut': str(disabled_shortcut.shortcut),
            'shortcut_full': f'{settings.host}{disabled_shortcut.shortcut}',
            'status_code': disabled_shortcut.status_code,
            'disabled': disabled_shortcut.disabled,
        }
    ], 'Response from GET request to `/api/` endpoint differs from expected'
