import logging
import string

from pydantic_settings import BaseSettings

SHORTCUT_LETTERS = string.ascii_letters + string.digits

class Config(BaseSettings):
    db_url: str
    host: str
    shortcut_auto_length: int
    log_level: str = 'INFO'


settings = Config()
