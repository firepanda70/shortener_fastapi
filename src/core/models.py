import re

from sqlalchemy import MetaData
from sqlalchemy.orm import declared_attr, DeclarativeBase

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class BaseDBModel(DeclarativeBase):
    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

    @declared_attr
    def __tablename__(cls):
        names = re.split("(?=[A-Z])", cls.__name__)
        return "_".join([x.lower() for x in names if x])
