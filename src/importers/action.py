from datetime import datetime
from src.models.action import Action
from src.crud import persist


def persist_action(card):  # TODO: Need to add connections
    instance = Action(
        card_id=card['id'],
        user_id='code_me',
        type='code_me',
        data='code_me',
        created_at=datetime.fromtimestamp(
            'code_me' / 1000
        )
    )
    unique_keys = {
        'card_id': instance.code_me,
        'data': instance.code_me,
        'created_at': instance.code_me
    }
    return persist(instance, unique_keys)
