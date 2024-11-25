from datetime import datetime
from src.models.card_label import CardLabel
from src.crud import persist


def persist_card_label(card):
    instance = CardLabel(
        card_id=card['planka_id'],
        label_id='',  # TODO: persist Label
        create_at=''
    )
    unique_keys = {
        'card_id': instance.card_id,
        'label_id': instance.label_id
    }
    return persist(instance, unique_keys)
