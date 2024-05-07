from fastapi import Depends

from .exceptions import ShortcutNotFound, ShortcutDisabled
from .services import get_shortcut_service, ShortcutServce
from .models import Shortcut


async def existing(
    id: str, service: ShortcutServce = Depends(get_shortcut_service)
) -> Shortcut:
    obj = await service.get_one(id)
    if not obj:
        raise ShortcutNotFound
    return obj

async def enabled(obj: Shortcut = Depends(existing)) -> Shortcut:
    if obj.disabled:
        raise ShortcutDisabled
    return obj
