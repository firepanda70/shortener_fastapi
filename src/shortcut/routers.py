from fastapi import APIRouter, Depends, status, Body

from .services import get_shortcut_service, ShortcutServce
from .dependencies import existing
from .schemas import (
    ShortcutCreate, ShortcutDB, ShortcutUpdate
)
from .models import Shortcut
from .openapi import *

shortcut_router = APIRouter()


@shortcut_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_SHORTCUT_RESPONSES
)
async def create_one(
    shortcut_data: ShortcutCreate = Body(
        title='ShortcutCreate',
        openapi_examples=CREATE_SHORTCUT_BODY_EXAMPLES,
        description='Request body with new shortcut data'
    ),
    service: ShortcutServce = Depends(get_shortcut_service)
) -> ShortcutDB:
    '''
    Creates new shortcut object

    Body params: 
    * **url** Required. URL in correct format (http://www.example.org). Recursive shortcuts not allowed
    * **status_code** Optional. HTTP status code for redirect response. Integer in range 300-309
    '''
    return await service.create_one(shortcut_data)


@shortcut_router.get(
    '/', status_code=status.HTTP_200_OK,
    responses=GET_SHORTCUT_RESPONSES
)
async def get_many(
    include_disabled: bool | None = None,
    service: ShortcutServce = Depends(get_shortcut_service)
) -> list[ShortcutDB]:
    '''
    Returns all existing shortcut objects

    Path params: 
    * **include_disabled** Optional. Include disabled shortcuts in response. Default `false`
    '''
    if include_disabled is None:
        include_disabled = False
    return await service.get_many(include_disabled)


@shortcut_router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    responses=UPDATE_SHORTCUT_RESPONSES
)
async def update_one(
    db_obj: Shortcut = Depends(existing),
    update_data: ShortcutUpdate = Body(
        title='ShortcutUpdate',
        openapi_examples=UPDATE_SHORTCUT_BODY_EXAMPLES
    ),
    service: ShortcutServce = Depends(get_shortcut_service)
) -> ShortcutDB:
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
    return await service.update_one(db_obj, update_data)


@shortcut_router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK,
    responses=DELETE_SHORTCUT_RESPONSES
)
async def delete_one(
    db_obj: Shortcut = Depends(existing),
    service: ShortcutServce = Depends(get_shortcut_service)
) -> ShortcutDB:
    '''
    Deletes exising shortcut by string identifier

    Path params:
    * **shortcut** Required. Unique string shortcut identifier.
    '''
    return await service.delete_one(db_obj)
