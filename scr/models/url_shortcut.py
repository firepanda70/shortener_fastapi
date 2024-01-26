from sqlalchemy.orm import Mapped, mapped_column

from scr.core.db import BaseDBModel


class URLShortcut(BaseDBModel):
    url: Mapped[str]
    shortcut: Mapped[str] = mapped_column(unique=True)
    status_code: Mapped[int]
    disabled: Mapped[bool]
