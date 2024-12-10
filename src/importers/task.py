from src.crud import persist
from src.models.task import Task


def persist_task(
    task,
    card_id,
    created_at,
    position,
    session,
    context
):
    instance = Task(
        card_id=card_id,
        name=task['name'],
        is_completed=task['isCompleted'],
        created_at=created_at,
        position=position
    )
    unique_keys = {
        'name': instance.name,
        'card_id': instance.card_id,
        'created_at': instance.created_at
    }
    return persist(
        instance=instance,
        unique_keys=unique_keys,
        session=session,
        context=context
    )
