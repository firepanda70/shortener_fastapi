from datetime import datetime

from pydantic import (
    BaseModel, AnyHttpUrl, Field, field_validator,
    computed_field, field_serializer, SerializationInfo, ValidationInfo
)

from src.core.config import settings, SHORTCUT_LETTERS
from src.core.schemas import CustomBase, CustomBaseDB


class ShortcutBase(BaseModel):
    url: AnyHttpUrl = Field(..., description='URL to create shortcut to.')
    status_code: int = Field(301, gt=299, lt=309, description='Redirect status code')


class ShortcutCreate(ShortcutBase, CustomBase):
    '''
    Shortcut object create schema
    '''
    @field_validator('url')
    @classmethod
    def url_not_recursive(cls, url: AnyHttpUrl, info: ValidationInfo) -> AnyHttpUrl:
        if str(url).find(settings.host) == 0:
            raise ValueError('Recursive shortcuts are forbidden')
        return url


class ShortcutUpdate(CustomBase):
    '''
    Shortcut object update schema
    '''
    url: AnyHttpUrl | None = Field(None, description='URL to create shortcut to')
    status_code: int | None = Field(None, gt=299, lt=309, description='Redirect status code')
    disabled: bool | None = Field(None, description='Disabled/enabled shortcut avaliability')
    id: str | None = Field(
        None, max_length=16, validation_alias='shortcut',
        description='Shortcut unique string identifier. Max length - 16'
    )

    @field_validator('url')
    @classmethod
    def url_not_recursive(cls, url: AnyHttpUrl | None, info: ValidationInfo) -> AnyHttpUrl:
        '''
        Validates shortcut URL is not recursive
        '''
        if url is not None and str(url).find(settings.host) == 0:
            raise ValueError('Recursive shortcuts are forbidden')
        return url
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, id: str | None, info: ValidationInfo) -> str:
        '''
        Validates shortcut contains only allowed symbols
        '''
        if id and not all([symbol in SHORTCUT_LETTERS for symbol in id]):
            raise ValueError('Shortcut must contain only ASCII letters and digits')
        return id

    @field_serializer('url')
    def serialize_url(self, url: AnyHttpUrl, _info: SerializationInfo) -> str:
        return str(url)


class ShortcutDB(ShortcutBase, CustomBaseDB):
    '''
    Shortcut object database schema
    '''
    id: str = Field(..., description='DB object identifier', serialization_alias='shortcut')
    disabled: bool = Field(..., description='Disabled/enabled shortcut avaliability')
    created_at: datetime = Field(..., description='Date object was created')
    updated_at: datetime = Field(..., description='Date object was updated last time')

    @computed_field
    @property
    def shortcut_full(self) -> str:
        '''Full shortcut URL'''
        return settings.host + self.id
