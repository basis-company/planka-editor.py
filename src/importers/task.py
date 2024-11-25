from datetime import datetime
from src.models.action import Action
from src.crud import persist


def persist_task(card):  # TODO: Need to add connections
    instance = Task(
        card_id=card['id'],
        name='code_me',
        is_completed='code_me',
        created_at=datetime.fromtimestamp(
            'code_me' / 1000
        ),
        position='code_me'
    )
    unique_keys = {
        'card_id': instance.code_me,
        'name': instance.code_me,
        'is_completed': instance.code_me,
        'created_at': instance.code_me
    }
    return persist(instance, unique_keys)
