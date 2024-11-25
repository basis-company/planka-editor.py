from datetime import datetime
from src.models.card_membership import CardMembership
from src.crud import persist


def persist_card_membership(card):
    instance = CardMembership(
        card_id=card['id'],
        user_id=card['planka_card_membership']['planka_user_id'],
        created_at=datetime.fromtimestamp(
            card['planka_card_membership']['planka_created_at'] / 1000
        )
    )
    unique_keys = {
        'card_id': instance.card_id,
        'user_id': instance.user_id
    }
    return persist(instance, unique_keys)
