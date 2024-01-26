from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from scr.models import URLShortcut
from scr.schemas import (
    URLShortcutCreate, URLShortcutUpdate
)


class URLShortcurRepo:

    async def create_one(
        self, obj_in: URLShortcutCreate,
        shortcut: str, session: AsyncSession
    ) -> URLShortcut:
        now = datetime.now()
        url_shortcut = URLShortcut(
            created_at=now, updated_at=now, shortcut=shortcut,
            url=str(obj_in.url), status_code=obj_in.status_code,
            disabled=False
        )
        session.add(url_shortcut)
        await session.commit()
        await session.refresh(url_shortcut)
        return url_shortcut

    async def get_one_by_shorcut(
        self, shortcut: str, session: AsyncSession
    ) -> URLShortcut | None:
        res = await session.execute(
            select(URLShortcut).where(URLShortcut.shortcut == shortcut)
        )
        return res.scalar_one_or_none()

    async def get_many(
        self, session: AsyncSession, include_disabled: bool
    ) -> list[URLShortcut]:
        expr = select(URLShortcut)
        if not include_disabled:
            expr = expr.where(URLShortcut.disabled == False)
        return (await session.execute(expr)).scalars().all()

    async def update_one(
        self, db_obj: URLShortcut,
        update_data: URLShortcutUpdate, session: AsyncSession
    ) -> URLShortcut:
        update_obj_data = update_data.model_dump(exclude_none=True)
        update_obj_data['updated_at'] = datetime.now()
        for attr, value in update_obj_data.items():
            setattr(db_obj, attr, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete_one(
        self, db_obj: URLShortcut, session: AsyncSession
    ) -> URLShortcut:
        await session.delete(db_obj)
        await session.commit()
        return db_obj


url_shortcut_repo = URLShortcurRepo()
