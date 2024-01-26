from sqlalchemy.ext.asyncio import AsyncSession

from scr.schemas import URLShortcutCreate, URLShortcutUpdate
from scr.repos import url_shortcut_repo
from scr.models import URLShortcut
from scr.core.config import settings
from .exceptions import ShortcutNotFound, ShortcutDisabled, ShortcutTaken
from .utils import get_random_string


class URLShortcutService:

    async def create_one(
        self, obj_in: URLShortcutCreate, session: AsyncSession
    ) -> URLShortcut:
        length = settings.shortcut_min_length
        while True:
            shortcut = await get_random_string(length)
            db_obj = await url_shortcut_repo.get_one_by_shorcut(shortcut, session)
            if db_obj is None:
                break
            length += 1
        return await url_shortcut_repo.create_one(obj_in, shortcut, session)

    async def get_one_by_shorcut(
        self, shortcut: str, session: AsyncSession
    ) -> URLShortcut:
        obj = await url_shortcut_repo.get_one_by_shorcut(shortcut, session)
        if not obj:
            raise ShortcutNotFound(shortcut)
        return obj

    async def get_enabled_shotcut(
        self, shortcut: str, session: AsyncSession
    ) -> URLShortcut:
        obj = await self.get_one_by_shorcut(shortcut, session)
        if obj.disabled:
            raise ShortcutDisabled(shortcut)
        return obj

    async def get_many(
        self, session: AsyncSession, include_disabled: bool
    ) -> list[URLShortcut]:
        return await url_shortcut_repo.get_many(session, include_disabled)

    async def update_one(
        self, shortcut: str, update_data: URLShortcutUpdate, session: AsyncSession
    ) -> URLShortcut:
        db_obj = await self.get_one_by_shorcut(shortcut, session)
        if update_data.shortcut is not None:
            conficted_obj = await url_shortcut_repo.get_one_by_shorcut(
                update_data.shortcut, session
            )
            if conficted_obj is not None and conficted_obj.id != db_obj.id:
                raise ShortcutTaken(update_data.shortcut)
        return await url_shortcut_repo.update_one(db_obj, update_data, session)

    async def delete_one(self, shortcut: str, session: AsyncSession) -> URLShortcut:
        db_obj = await self.get_one_by_shorcut(shortcut, session)
        return await url_shortcut_repo.delete_one(db_obj, session)


url_shortcut_service = URLShortcutService()
