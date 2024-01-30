from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.db import get_async_session
from scr.services import url_shortcut_service
from scr.schemas import (
    URLShortcutCreate, URLShortcutDB, URLShortcutUpdate
)
from .examples import *

api_router = APIRouter(prefix='/api', tags=['url_shortener'])


@api_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_SHORTCUT_RESPONSES
)
async def create_one(
    shortcut_data: URLShortcutCreate = Body(
        title='URLShortcutCreate',
        openapi_examples=CREATE_SHORTCUT_BODY_EXAMPLES,
        description='Request body with new shortcut data'
    ),
    session: AsyncSession = Depends(get_async_session)
) -> URLShortcutDB:
    '''
    Creates new shortcut object

    Body params: 
    * **url** Required. URL in correct format (http://www.example.org). Recursive shortcuts not allowed
    * **status_code** Optional. HTTP status code for redirect response. Integer in range 300-309
    '''
    return await url_shortcut_service.create_one(shortcut_data, session)


@api_router.get(
    '/', status_code=status.HTTP_200_OK,
    responses=GET_SHORTCUT_RESPONSES
)
async def get_many(
    include_disabled: bool | None = None,
    session: AsyncSession = Depends(get_async_session)
) -> list[URLShortcutDB]:
    '''
    Returns all existing shortcut objects

    Path params: 
    * **include_disabled** Optional. Include disabled shortcuts in response. Default `false`
    '''
    if include_disabled is None:
        include_disabled = False
    return await url_shortcut_service.get_many(session, include_disabled)


@api_router.patch(
    '/{shortcut}',
    status_code=status.HTTP_200_OK,
    responses=UPDATE_SHORTCUT_RESPONSES
)
async def update_one(
    shortcut: str, update_data: URLShortcutUpdate = Body(
        title='URLShortcutUpdate',
        openapi_examples=UPDATE_SHORTCUT_BODY_EXAMPLES
    ),
    session: AsyncSession = Depends(get_async_session)
) -> URLShortcutDB:
    '''
    Updates existing shortcut object

    Path params:
    * **shortcut** Required. Unique string shortcut identifier.

    Body params: 
    * **url** Optional. URL in correct format (http://www.example.org). Recursive shortcuts not allowed
    * **status_code** Optional. HTTP status code for redirect response. Integer in range 300-309
    * **disabled** Optional. Disables/enables shortcut.
    * **shortcut** Optional. Sets custom shortcut string identifier. Must contain ocly ASCII letters and digits.
    '''
    return await url_shortcut_service.update_one(shortcut, update_data, session)


@api_router.delete(
    '/{shortcut}',
    status_code=status.HTTP_200_OK,
    responses=DELETE_SHORTCUT_RESPONSES
)
async def delete_one(
    shortcut: str, session: AsyncSession = Depends(get_async_session)
) -> URLShortcutDB:
    '''
    Deletes exising shortcut by string identifier

    Path params:
    * **shortcut** Required. Unique string shortcut identifier.
    '''
    return await url_shortcut_service.delete_one(shortcut, session)
