import string

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

SHORTCUT_LETTERS = string.ascii_letters + string.digits
LOG_FORMAT = "%(levelname)s:     %(message)s"


class Config(BaseSettings):
    db_url: PostgresDsn
    host: str
    shortcut_auto_length: int
    log_level: str = 'INFO'


settings = Config()
