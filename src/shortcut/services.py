import logging
from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_async_session
from .schemas import ShortcutCreate, ShortcutUpdate
from .models import Shortcut
from .utils import gen_rand_str
from .exceptions import ShortcutTaken

logger = logging.getLogger(__name__)


class ShortcutServce:
    '''
    Contains all buisness logic and DB requests
    '''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __gen_new_id(self) -> str:
        length = settings.shortcut_auto_length
        while True:
            id = await gen_rand_str(length)
            db_obj = await self.get_one(id)
            if db_obj is None:
                return id
            length += 1

    async def create_one(self, obj_in: ShortcutCreate) -> Shortcut:
        id = await self.__gen_new_id()
        url_shortcut = Shortcut(
            id=id, url=str(obj_in.url), disabled=False,
            status_code=obj_in.status_code
        )
        self.session.add(url_shortcut)
        await self.session.commit()
        await self.session.refresh(url_shortcut)
        logger.info(f'URLShortcut {url_shortcut.id} object created')
        return url_shortcut

    async def get_one(self, id: str) -> Shortcut | None:
        res = await self.session.execute(
            select(Shortcut).where(Shortcut.id == id)
        )
        return res.scalar_one_or_none()

    async def get_many(self, include_disabled: bool) -> Sequence[Shortcut]:
        expr = select(Shortcut)
        if not include_disabled:
            expr = expr.where(Shortcut.disabled == False)
        return (await self.session.execute(expr)).scalars().all()

    async def update_one(
        self, db_obj: Shortcut, update_data: ShortcutUpdate
    ) -> Shortcut:
        if update_data.id and update_data.id != db_obj.id:
            if await self.get_one(update_data.id):
                raise ShortcutTaken
        update_obj_data = update_data.model_dump(exclude_none=True)
        for attr, value in update_obj_data.items():
            setattr(db_obj, attr, value)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        logger.info(f'URLShortcut {db_obj.id} object updated')
        return db_obj

    async def delete_one(
        self, db_obj: Shortcut
    ) -> Shortcut:
        await self.session.delete(db_obj)
        await self.session.commit()
        logger.info(f'URLShortcut {db_obj.id} object deleted')
        return db_obj


async def get_shortcut_service(
    session: AsyncSession = Depends(get_async_session)
) -> ShortcutServce:
    return ShortcutServce(session)
