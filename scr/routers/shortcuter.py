from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.db import get_async_session
from scr.services import url_shortcut_service

shortcuter_router = APIRouter(include_in_schema=False)


@shortcuter_router.get('/{shortcut}')
async def get_redirect(
    shortcut: str, session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:
    obj = await url_shortcut_service.get_enabled_shotcut(shortcut, session)
    return RedirectResponse(status_code=obj.status_code, url=obj.url)
