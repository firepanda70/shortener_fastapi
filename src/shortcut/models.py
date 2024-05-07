from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import BaseDBModel


class Shortcut(BaseDBModel):
    id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    url: Mapped[str]
    status_code: Mapped[int]
    disabled: Mapped[bool]
