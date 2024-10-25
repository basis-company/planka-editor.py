from typing import Dict, Any, Optional, Type, TypeVar

from src.services.database import create_sqlalchemy_session
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


def persist(instance: T, unique_keys: Dict[str, Any]) -> Optional[T]:
    with database() as session:
        existing_instance = (
            session.query(type(instance))
            .filter_by(**unique_keys)
            .first()
        )
        if existing_instance:
            return None
        
        session.add(instance)
        session.commit()

        return instance


def get_instance(cls: Type[T], id: int) -> T:
    with database() as session:
        instance = session.get(cls, id)
        if not instance:
            raise LookupError(f'Instance {id} not found')

        return instance
