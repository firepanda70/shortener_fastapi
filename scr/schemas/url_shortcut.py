from datetime import datetime

from pydantic import (
    BaseModel, AnyHttpUrl, Field, ConfigDict, field_validator,
    computed_field, field_serializer
)

from scr.core.config import settings, SHORTCUT_LETTERS


class URLShortcutCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    url: AnyHttpUrl
    status_code: int = Field(301, gt=299, lt=309)

    @field_validator('url')
    @classmethod
    def url_not_recursive(cls, v: AnyHttpUrl) -> AnyHttpUrl:
        if str(v).find(settings.host) == 0:
            raise ValueError('Recursive shortcuts are forbidden')
        return v


class URLShortcutUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    url: AnyHttpUrl | None = Field(None)
    status_code: int | None = Field(None, gt=299, lt=309)
    disabled: bool | None = Field(None)
    shortcut: str | None = Field(None)

    @field_validator('url')
    @classmethod
    def url_not_recursive(cls, url: AnyHttpUrl | None) -> AnyHttpUrl:
        if url is not None and str(url).find(settings.host) == 0:
            raise ValueError('Recursive shortcuts are forbidden')
        return url
    
    @field_validator('shortcut')
    @classmethod
    def validate_shortcut(cls, shortcut: str | None) -> str:
        if len(shortcut) >= 10:
            raise ValueError('Shortcut length must be less than 10')
        if shortcut is not None:
            for symbol in shortcut:
                if symbol not in SHORTCUT_LETTERS:
                    raise ValueError('Shortcut must contain only ASCII letters and digits')
        return shortcut

    @field_serializer('url')
    def serialize_url(self, url: AnyHttpUrl, _info) -> str:
        return str(url)


class URLShortcutDB(URLShortcutCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    disabled: bool
    shortcut: str
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def shortcut_full(self) -> str:
        return settings.host + str(self.shortcut)
