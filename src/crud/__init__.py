from typing import Optional, Type, TypeVar

from services.database import create_sqlalchemy_session
from sqlalchemy.orm import Session

T = TypeVar('T')


def database() -> Session:
    session: Optional[Session] = None
    try:
        session = create_sqlalchemy_session()
        return session
    finally:
        if session is not None and session.is_active:
            session.close()


def persist(instance: T) -> T:
    with database() as session:
        session.add(instance)
        session.commit()

        return instance


def get_instance(cls: Type[T], id: int) -> T:
    with database() as session:
        instance = session.get(cls, id)
        if not instance:
            raise LookupError(f'Instance {id} not found')

        return instance
