from datetime import datetime
from src.models.task import Task
from src.crud import persist


def persist_task(task, card_id, created_at):
    instance = Task(
        card_id=card_id,
        name=task['name'],
        is_completed=task['isCompleted'],
        created_at=datetime.fromtimestamp(
            created_at / 1000
        ),
        position='code_me'
    )
    unique_keys = {
        'name': instance.name,
        'card_id': instance.card_id,
        'created_at': instance.created_at
    }
    return persist(instance, unique_keys)
