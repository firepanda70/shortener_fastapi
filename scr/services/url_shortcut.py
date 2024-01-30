import logging

from sqlalchemy.ext.asyncio import AsyncSession

from scr.schemas import URLShortcutCreate, URLShortcutUpdate
from scr.repos import url_shortcut_repo
from scr.models import URLShortcut
from scr.core.config import settings
from scr.exceptions import ShortcutNotFound, ShortcutDisabled, ShortcutTaken
from scr.utils import get_random_string


logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)


class URLShortcutService:
    '''
    Contains buisness-logic and actions related with `URLShortcut` DB model
    '''

    async def create_one(
        self, obj_in: URLShortcutCreate, session: AsyncSession
    ) -> URLShortcut:
        '''
        Creates new `URLShortcut` DB object, generates unique shortcut string identifier
        '''
        length = settings.shortcut_auto_length
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
        '''
        Returns existing shortcut object.
        Raises `scr.exceptions.ShortcutNotFound` if object does not exist.
        '''
        obj = await url_shortcut_repo.get_one_by_shorcut(shortcut, session)
        if not obj:
            logger.warning(
                f'Invalid request: URLShortcut obj with shortcut {shortcut} does not exists'
            )
            raise ShortcutNotFound(shortcut)
        return obj

    async def get_enabled_shotcut(
        self, shortcut: str, session: AsyncSession
    ) -> URLShortcut:
        '''
        Returns existing shortcut object with enabled status.
        Raises `scr.exceptions.ShortcutNotFound` if object does not exist.
        Raises `scr.exceptions.ShortcutDisabled` if disabled.
        '''
        obj = await self.get_one_by_shorcut(shortcut, session)
        if obj.disabled:
            logger.warning(
                f'Invalid request: URLShortcut obj with shortcut {shortcut} is disabled'
            )
            raise ShortcutDisabled(shortcut)
        return obj

    async def get_many(
        self, session: AsyncSession, include_disabled: bool
    ) -> list[URLShortcut]:
        '''
        Returns all shortcut objects from DB.
        '''
        return await url_shortcut_repo.get_many(session, include_disabled)

    async def update_one(
        self, shortcut: str, update_data: URLShortcutUpdate, session: AsyncSession
    ) -> URLShortcut:
        '''
        Updates existing shortcut object.
        Raises `scr.exceptions.ShortcutNotFound` if object does not exist.
        Raises `scr.exceptions.ShortcutTaken` if new string shortcut identified is already taken (if provided)
        '''
        db_obj = await self.get_one_by_shorcut(shortcut, session)
        if update_data.shortcut is not None:
            conficted_obj = await url_shortcut_repo.get_one_by_shorcut(
                update_data.shortcut, session
            )
            if conficted_obj is not None and conficted_obj.id != db_obj.id:
                logger.warning(
                    f'Invalid request: URLShortcut obj with shortcut {shortcut} already exists'
                )
                raise ShortcutTaken(update_data.shortcut)
        return await url_shortcut_repo.update_one(db_obj, update_data, session)

    async def delete_one(self, shortcut: str, session: AsyncSession) -> URLShortcut:
        '''
        Deletes existing URLShortcut object from DB.
        Raises `scr.exceptions.ShortcutNotFound` if object does not exist.
        '''
        db_obj = await self.get_one_by_shorcut(shortcut, session)
        return await url_shortcut_repo.delete_one(db_obj, session)


url_shortcut_service = URLShortcutService()
