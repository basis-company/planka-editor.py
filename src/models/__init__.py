from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    def dict(self) -> dict:
        base_inspect = inspect(self)
        if base_inspect is None:
            raise LookupError('Cant inspect instance')

        return {column.key: getattr(self, column.key)
                for column in base_inspect.mapper.column_attrs}
