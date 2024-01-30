from datetime import datetime

from pydantic import (
    BaseModel, AnyHttpUrl, Field, ConfigDict, field_validator,
    computed_field, field_serializer
)

from scr.core.config import settings, SHORTCUT_LETTERS


class URLShortcutCreate(BaseModel):
    '''
    Shortcut object create schema
    '''
    model_config = ConfigDict(extra='forbid')

    url: AnyHttpUrl = Field(..., description='URL to create shortcut to.')
    status_code: int = Field(301, gt=299, lt=309, description='Redirect status code')

    @field_validator('url')
    @classmethod
    def url_not_recursive(cls, url: AnyHttpUrl) -> AnyHttpUrl:
        if str(url).find(settings.host) == 0:
            raise ValueError('Recursive shortcuts are forbidden')
        return url


class URLShortcutUpdate(BaseModel):
    '''
    Shortcut object update schema
    '''
    model_config = ConfigDict(extra='forbid')

    url: AnyHttpUrl | None = Field(None, description='URL to create shortcut to')
    status_code: int | None = Field(None, gt=299, lt=309, description='Redirect status code')
    disabled: bool | None = Field(None, description='Disabled/enabled shortcut avaliability')
    shortcut: str | None = Field(
        None, max_length=16,
        description='Shortcut unique string identifier. Max length - 16'
    )

    @field_validator('url')
    @classmethod
    def url_not_recursive(cls, url: AnyHttpUrl | None) -> AnyHttpUrl:
        '''
        Validates shortcut URL is not recursive
        '''
        if url is not None and str(url).find(settings.host) == 0:
            raise ValueError('Recursive shortcuts are forbidden')
        return url
    
    @field_validator('shortcut')
    @classmethod
    def validate_shortcut(cls, shortcut: str | None) -> str:
        '''
        Validates shortcut contains only allowed symbols
        '''
        if shortcut is not None:
            for symbol in shortcut:
                if symbol not in SHORTCUT_LETTERS:
                    raise ValueError('Shortcut must contain only ASCII letters and digits')
        return shortcut

    @field_serializer('url')
    def serialize_url(self, url: AnyHttpUrl, _info) -> str:
        return str(url)


class URLShortcutDB(URLShortcutCreate):
    '''
    Shortcut object database schema
    '''
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='DB object identifier')
    disabled: bool = Field(..., description='Disabled/enabled shortcut avaliability')
    shortcut: str = Field(..., description='Shortcut unique string identifier')
    created_at: datetime = Field(..., description='Date object was created')
    updated_at: datetime = Field(..., description='Date object was updated last time')

    @computed_field
    @property
    def shortcut_full(self) -> str:
        '''Full shortcut URL'''
        return settings.host + self.shortcut
