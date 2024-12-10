from src.models.card_label import CardLabel
from src.crud import persist


def persist_card_label(
    label_id,
    card_id,
    created_at,
    session,
    context
):
    instance = CardLabel(
        card_id=card_id,
        label_id=label_id,
        created_at=created_at
    )
    unique_keys = {
        'card_id': instance.card_id,
        'label_id': instance.label_id
    }
    return persist(
        instance=instance,
        unique_keys=unique_keys,
        session=session,
        context=context
    )
