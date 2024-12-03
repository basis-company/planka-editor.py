from datetime import datetime, timedelta

from src.models.action import Action
from src.services.timestamp import timestamp_format
from src.crud import persist


def persist_action(action, card_id, context):
    data = {
        "text": action['data']
    }
    instance = Action(
        card_id=card_id,
        user_id=action['user_id'],
        type="commentCard",
        data=data,
        created_at=timestamp_format(action['created_at'], timezone=True)
    )
    unique_keys = {
        'card_id': instance.card_id,
        'data': instance.data,
        'created_at': instance.created_at
    }
    return persist(instance, unique_keys, context=context)
