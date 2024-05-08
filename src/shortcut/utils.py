import random

from src.core.config import SHORTCUT_LETTERS


async def gen_rand_str(length: int):
    return ''.join(random.choice(SHORTCUT_LETTERS) for _ in range(length))
