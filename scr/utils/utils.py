import random
import string
from scr.core.config import SHORTCUT_LETTERS


async def get_random_string(length: int):
    return ''.join(random.choice(SHORTCUT_LETTERS) for _ in range(length))
