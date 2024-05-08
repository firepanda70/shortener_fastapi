'''
TODO:
Tests for redirect responses
Tests for disabled shortcuts redirect responses
Tests for non existent shortcuts
Tests for shortcut deletion
Refactor
'''

import string
from datetime import datetime
from typing import Any

import pytest

from src.core.config import settings
from src.shortcut.models import Shortcut
from tests.conftest import test_client
from .common import validate_keys

SHORTCUT_LETTERS = string.ascii_letters + string.digits
API_ENDPOINT = '/api/v1/shortcut/'


@pytest.mark.parametrize(
    'invalid_url',
    [
        'not_url',
        '',
        None,
        f'{settings.host}/recursive_url'
    ],
)
def test_create_shortcut_invalid_url(invalid_url: Any):
    response = test_client.post(
        API_ENDPOINT,
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
def test_create_shortcut_invalid_status_code(status_code: Any):
    response = test_client.post(
        API_ENDPOINT,
        json={
            'url': 'https://ya.ru/',
            'status_code': status_code
        },
    )
    assert (
        response.status_code == 422
    ), 'Status code of shortcut must be integer 299 < x < 309'


@pytest.mark.parametrize('json', [
    {'shortcut': 'shortcut'},
    {'disabled': True},
    {'created_at': '2024-01-01T00:00:00'},
    {'updated_at': '2024-01-01T00:00:00'},
    {'shortcut_full': f'{settings.host}/shortcut'},
])
def test_create_shortcut_with_autofilling_fields(json: dict[str, Any]):
    response = test_client.post(
        API_ENDPOINT,
        json={
            'url': 'https://ya.ru/',
            'status_code': 301,
            **json
        }
    )
    assert (
        response.status_code == 422
    ), 'Autofill fields providing must be forbidden'


def test_get_shortcut(google_shortcut: Shortcut):
    response = test_client.get(API_ENDPOINT)
    assert (
        response.status_code == 200
    ), f'GET response to `{API_ENDPOINT}` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), f'GET response to `{API_ENDPOINT}` endpoint must return `list` object.'
    assert len(response.json()) == 1, (
        f'GET response to `{API_ENDPOINT}` endpoint did not return expected objects amount from DB'
    )
    data = response.json()[0]
    validate_keys(data)
    assert response.json() == [
        {
            'created_at': google_shortcut.created_at.isoformat(),
            'updated_at': google_shortcut.updated_at.isoformat(),
            'url': google_shortcut.url,
            'shortcut': google_shortcut.id,
            'shortcut_full': f'{settings.host}{google_shortcut.id}',
            'status_code': google_shortcut.status_code,
            'disabled': google_shortcut.disabled,
        }
    ], f'Response from GET request to `{API_ENDPOINT}` endpoint differs from expected'

def test_get_all_shortcuts(
    google_shortcut: Shortcut, ya_shortcut: Shortcut
):
    response = test_client.get(API_ENDPOINT)
    assert (
        response.status_code == 200
    ), f'GET response to `{API_ENDPOINT}` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), f'GET response to `{API_ENDPOINT}` endpoint must return `list` object.'
    assert len(response.json()) == 2, (
        f'GET response to `{API_ENDPOINT}` endpoint did not return expected objects amount from DB'
    )
    data = response.json()[0]
    validate_keys(data)
    for shortcut in (google_shortcut, ya_shortcut):
        assert (
            {
                'created_at': shortcut.created_at.isoformat(),
                'updated_at': shortcut.updated_at.isoformat(),
                'url': shortcut.url,
                'shortcut': shortcut.id,
                'shortcut_full': f'{settings.host}{shortcut.id}',
                'status_code': shortcut.status_code,
                'disabled': shortcut.disabled,
            } in response.json()
        ), f'Response from GET request to `{API_ENDPOINT}` endpoint differs from expected'

@pytest.mark.parametrize('json', [
    {'url': 'https://ya.ru/'},
    {'url': 'https://ya.ru/', 'status_code': 303},
])
def test_create_shortcut(json: dict[str, Any]):
    response = test_client.post(
        API_ENDPOINT,
        json=json,
    )
    assert (
        response.status_code == 201
    ), f'Response from POST request to `{API_ENDPOINT}` endpoint must return status code 201.'
    data = response.json()
    validate_keys(data)
    shortcut = data.pop('shortcut')
    data.pop('created_at')
    data.pop('updated_at')

    for symbol in shortcut:
        assert (
            symbol in SHORTCUT_LETTERS
        ), 'Shortcut must contain only ASCII letters and digits'

    assert data == {
        'url': json['url'],
        'status_code': json['status_code'] if 'status_code' in json else 301,
        'shortcut_full': f'{settings.host}{shortcut}',
        'disabled': False
    }, f'Response from POST request to `{API_ENDPOINT}` endpoint differs from expected'

@pytest.mark.parametrize('json', [
    {'url': 'not_url'},
    {'status_code': 404},
    {'shortcut': '_=+^%# @'},
    {'shortcut': 'longname' * 10},
    {'created_at': '2024-01-02T00:00:00'},
    {'updated_at': '2024-01-02T00:00:00'},
    {'shortcut_full': f'{settings.host}shortcut'},
])
def test_update_one_invald_data(google_shortcut: Shortcut, json: dict[str, Any]):
    response = test_client.patch(
        f'{API_ENDPOINT}{google_shortcut.id}',
        json=json,
    )
    assert (
        response.status_code == 422
    ), 'Invalid or forbidden data was accepted on update'

def test_update_conflict_shortcut(
    google_shortcut: Shortcut, ya_shortcut: Shortcut
):
    response = test_client.patch(
        f'{API_ENDPOINT}{google_shortcut.id}',
        json={'shortcut': ya_shortcut.id},
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
def test_successfull_update(google_shortcut: Shortcut, json: dict[str, Any]):
    response = test_client.patch(
        f'{API_ENDPOINT}{google_shortcut.id}',
        json=json,
    )
    assert (
        response.status_code == 200
    ), f'PATCH request to `{API_ENDPOINT}` endpoint must return status code 200.'
    data = response.json()
    validate_keys(data)
    updated_at = datetime.fromisoformat(data.pop('updated_at'))
    created_at = datetime.fromisoformat(data.pop('created_at'))
    assert (
        updated_at > created_at,
    ), f'`updated_at` field shoud be updated on PATCH request to `{API_ENDPOINT}` endpoint'
    assert data == {
        'url': json['url'],
        'status_code': (
            json['status_code']
            if 'status_code' in json
            else google_shortcut.status_code
        ),
        'shortcut': (
            json['shortcut'] if 'shortcut' in json
            else str(google_shortcut.id)
        ),
        'shortcut_full': f'{settings.host}{
            json['shortcut'] if 'shortcut' in json
            else str(google_shortcut.id)
        }',
        'disabled': (
            json['disabled'] if 'disabled' in json
            else google_shortcut.disabled
        ),
    }, f'Response from PATCH request to `{API_ENDPOINT}{google_shortcut.id}` endpoint differs from expected'


def test_disabled_shortcut(disabled_shortcut: Shortcut):
    response = test_client.get(API_ENDPOINT)
    assert (
        response.status_code == 200
    ), f'GET request to `{API_ENDPOINT}` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), f'GET request to `{API_ENDPOINT}` endpoint must return `list` object.'
    assert len(response.json()) == 0, (
        'Disabled shortcuts should not be returned by default'
    )

    response = test_client.get(API_ENDPOINT, params={'include_disabled': True})
    assert (
        response.status_code == 200
    ), f'GET request to `{API_ENDPOINT}` endpoint must return status code 200.'
    assert isinstance(
        response.json(), list
    ), f'GET request to `{API_ENDPOINT}` endpoint must return `list` object.'
    assert len(response.json()) == 1, (
        'GET request did not return expected objects amount from DB'
    )
    data = response.json()[0]
    validate_keys(data)
    data.pop('created_at')
    data.pop('updated_at')
    assert data == {
        'url': disabled_shortcut.url,
        'shortcut': disabled_shortcut.id,
        'shortcut_full': f'{settings.host}{disabled_shortcut.id}',
        'status_code': disabled_shortcut.status_code,
        'disabled': disabled_shortcut.disabled,
    } , f'Response from GET request to `{API_ENDPOINT}` endpoint differs from expected'
