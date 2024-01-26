from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.db import get_async_session
from scr.services import url_shortcut_service
from scr.schemas import (
    URLShortcutCreate, URLShortcutDB, URLShortcutUpdate
)

api_router = APIRouter(prefix='/api', tags=['url_shortener'])


@api_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_one(
    obj_in: URLShortcutCreate,
    session: AsyncSession = Depends(get_async_session)
) -> URLShortcutDB:
    return await url_shortcut_service.create_one(obj_in, session)


@api_router.get('/', status_code=status.HTTP_200_OK)
async def get_many(
    include_disabled: bool | None = None,
    session: AsyncSession = Depends(get_async_session)
) -> list[URLShortcutDB]:
    if include_disabled is None:
        include_disabled = False
    return await url_shortcut_service.get_many(session, include_disabled)


@api_router.patch('/{shortcut}', status_code=status.HTTP_200_OK)
async def update_one(
    shortcut: str, update_data: URLShortcutUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> URLShortcutDB:
    return await url_shortcut_service.update_one(shortcut, update_data, session)


@api_router.delete('/{shortcut}', status_code=status.HTTP_200_OK)
async def delete_one(
    shortcut: str, session: AsyncSession = Depends(get_async_session)
) -> URLShortcutDB:
    return await url_shortcut_service.delete_one(shortcut, session)
