"""
Итерация 3: Импортируем метки на доски.
"""

from datetime import datetime
from src.models.label import Label

from src.crud import persist
from src.services.data import load_json, save_json


def persist_label(label):
    instance = Label(
        board_id=label['board_id'],
        name=label['name'],
        color=label['color'],
        created_at=label['created_at'],
        position=label['position']
    )
    unique_keys = {
        'card_id': instance.card_id,
        'label_id': instance.label_id
    }
    return persist(instance, unique_keys)
