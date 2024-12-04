"""
Итерация 3: Импортируем метки на доски.
"""
from src.models.label import Label

from src.crud import persist

from src.services.timestamp import timestamp_format


def persist_label(label, context):
    instance = Label(
        board_id=label['board_id'],
        name=label['name'],
        color=label['color'],
        created_at=timestamp_format(label['created_at']),
        position=label['board_position']
    )
    unique_keys = {
        'name': instance.name,
        'board_id': instance.board_id,
        'created_at': instance.created_at
    }
    
    return persist(
        instance,
        unique_keys,
        return_dublicate=True,
        context=context
    )
