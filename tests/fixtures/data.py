from datetime import datetime

import pytest

from scr.models.url_shortcut import URLShortcut


@pytest.fixture
def google_shortcut(freezer, mixer) -> URLShortcut:
    freezer.move_to('2024-01-01')
    return mixer.blend(
        'scr.models.url_shortcut.URLShortcut',
        created_at=datetime.now(), updated_at=datetime.now(),
        url='https://www.google.com/', shortcut='google2',
        status_code=301, disabled=False
    )

@pytest.fixture
def ya_shortcut(freezer, mixer) -> URLShortcut:
    freezer.move_to('2024-01-01')
    return mixer.blend(
        'scr.models.url_shortcut.URLShortcut',
        created_at=datetime.now(), updated_at=datetime.now(),
        url='https://ya.ru/', shortcut='ya2',
        status_code=302, disabled=False
    )

@pytest.fixture
def disabled_shortcut(freezer, mixer) -> URLShortcut:
    freezer.move_to('2024-01-01')
    return mixer.blend(
        'scr.models.url_shortcut.URLShortcut',
        created_at=datetime.now(), updated_at=datetime.now(),
        url='https://ya.ru/', shortcut='ya2',
        status_code=301, disabled=True
    )
