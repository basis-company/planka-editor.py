from typing import Dict, Any, Optional, Type, TypeVar
from src.models.transaction import TransactionContext

from src.services.database import create_sqlalchemy_session
# from src.services.data import load_json, save_json

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


def persist(
    instance: T,
    unique_keys: Optional[Dict[str, Any]] = None,
    return_dublicate: bool = False,
    session: Optional[Session] = None,
    context: Optional["TransactionContext"] = None
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
        session (Session, optional): Текущая сессия src.crud.database.
        context (TransactionContext, optional): Контекст текущей транзакции, для 
                                                логирования и работы сервиса undo.

    Returns:
        T | None: Возвращает объект сущности, если она была добавлена или найдена, 
                  или None, если сущность с такими ключами уже существует и return_dublicate=False.
    """
# with database() as session:
    if session is None:
        raise ValueError("[Error] No session provided to the persist method!")

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
    session.flush()
    # session.commit()

    # logging
    if context:
        context.write(type(instance).__name__, instance.id)

    return instance


def erase(
    entity_class,
    entity_id: int,
    session: Optional[Session] = None
) -> bool:
# with database() as session:
    if session is None:
        raise ValueError("[Error] No session provided to the erase method!")

    entity = session.query(entity_class).get(entity_id)
    if entity:
        session.delete(entity)
        session.flush()
        # session.commit()
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
