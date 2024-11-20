from typing import Dict, Any, Optional, Type, TypeVar, Union

from src.services.database import create_sqlalchemy_session
from src.services.data import load_json, save_json
from sqlalchemy.orm import Session

from constants import LOG_FILE_NAME

T = TypeVar('T')


def database() -> Session:
    session: Optional[Session] = None
    try:
        session = create_sqlalchemy_session()
        return session
    finally:
        if session is not None and session.is_active:
            session.close()


def persist(
    instance: T,
    unique_keys: Optional[Dict[str, Any]] = None,
    return_dublicate: bool = False
) -> Optional[T]:
    """
    Создает новую сущность в базе данных или возвращает уже существующую, если 
    она соответствует уникальным ключам из unique_keys.

    Если сущность с такими уникальными ключами уже существует, то по умолчанию 
    возвращает None. Если параметр return_dublicate установлен в True, возвращает 
    объект существующей сущности.

    Args:
        instance (T): Сущность для сохранения в базе данных.
        unique_keys (dict, optional): Уникальные ключи для поиска существующей сущности.
                                      Если не указаны, поиск не выполняется.
        return_dublicate (bool, optional): Флаг, указывающий, нужно ли возвращать 
                                           объект существующей сущности при нахождении дубликата.
                                           По умолчанию False.

    Returns:
        T | None: Возвращает объект сущности, если она была добавлена или найдена, 
                  или None, если сущность с такими ключами уже существует и return_dublicate=False.
    """
    with database() as session:
        if unique_keys is not None:
            existing_instance = (
                session.query(type(instance))
                .filter_by(**unique_keys)
                .first()
            )
            if existing_instance:
                if return_dublicate:
                    return existing_instance
                return None

        session.add(instance)
        session.commit()

        # execution logging
        uploaded_data = load_json(LOG_FILE_NAME)
        entity_name = type(instance).__name__
        if entity_name not in uploaded_data:
            uploaded_data[entity_name] = []
        uploaded_data[entity_name].append(instance.id)
        save_json(LOG_FILE_NAME, uploaded_data)

        return instance


def erase(entity_class, entity_id: int) -> bool:
    with database() as session:
        entity = session.query(entity_class).get(entity_id)
        if entity:
            session.delete(entity)
            session.commit()
            return True
        else:
            print(f"Сущность с id {entity_id} не найдена.")
            return False


def get_instance(cls: Type[T], id: int) -> T:
    with database() as session:
        instance = session.get(cls, id)
        if not instance:
            raise LookupError(f'Instance {id} not found')

        return instance
