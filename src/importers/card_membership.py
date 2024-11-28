from datetime import datetime
from src.models.card_membership import CardMembership
from src.crud import persist


def persist_card_membership(member, card_id, context):
    instance = CardMembership(
        card_id=card_id,
        user_id=member['planka_user_id'],
        created_at=datetime.fromtimestamp(
            member['planka_created_at'] / 1000
        )
    )
    unique_keys = {
        'card_id': instance.card_id,
        'user_id': instance.user_id
    }
    return persist(instance, unique_keys, context=context)
