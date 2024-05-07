from datetime import datetime

import pytest
from mixer.backend.sqlalchemy import Mixer

from src.shortcut.models import Shortcut


@pytest.fixture
def google_shortcut(mixer: Mixer) -> Shortcut:
    return mixer.blend(
        'src.shortcut.models.Shortcut',
        url='https://www.google.com/', id='google2',
        status_code=301, disabled=False
    )

@pytest.fixture
def ya_shortcut(mixer: Mixer) -> Shortcut:
    return mixer.blend(
        'src.shortcut.models.Shortcut',
        url='https://ya.ru/', id='ya2',
        status_code=302, disabled=False
    )

@pytest.fixture
def disabled_shortcut(mixer: Mixer) -> Shortcut:
    now = datetime.now()
    return mixer.blend(
        'src.shortcut.models.Shortcut',
        url='https://ya.ru/', id='ya2',
        status_code=301, disabled=True
    )
