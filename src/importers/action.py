from datetime import datetime
from src.models.action import Action
from src.crud import persist


def persist_action(action, card_id):
    instance = Action(
        card_id=card_id,
        user_id=action['user_id'],
        type="commentCard",
        data=action['data'],
        created_at=datetime.fromtimestamp(
            action['created_at'] / 1000
        )
    )
    unique_keys = {
        'card_id': instance.card_id,
        'data': instance.data,
        'created_at': instance.created_at
    }
    return persist(instance, unique_keys)
