from constants import LOG_FILE_NAME

from src.models.card import Card
from src.models.transaction import TransactionContext

from src.crud import persist
from src.services.data import load_json, save_json
from src.services.markdown import html_to_markdown
from src.services.timestamp import timestamp_format

from src.importers.label import persist_label
from src.importers.card_label import persist_card_label
from src.importers.card_membership import persist_card_membership
from src.importers.task import persist_task
from src.importers.action import persist_action
# from src.importers.attachment import identify_attachments


''' TODO:
[+] Card entity
    [+] due date and completion status
    [+] archived card placement logic
[+] CardLabel connection + persist Labels
[+] CardMembership entities
[+] Action entities (chat messages)
[+] Task entities (checklists)
[+] Add recursion for subtask
[ ] Add metadata to subtasks description and title (snippet)
'''


def save_transaction_log(context: TransactionContext):
    """Сохраняет лог транзакции в файл."""
    uploaded_data = load_json(LOG_FILE_NAME) or {}
    transaction_data = context.get_transaction_data()

    if not transaction_data["entities"]:
        return

    # uploaded_data[context.transaction_id] = {
    #     "timestamp": transaction_data["timestamp"],
    #     "entities": transaction_data["entities"]
    # }
    uploaded_data[transaction_data["timestamp"]] = transaction_data["entities"]
    save_json(LOG_FILE_NAME, uploaded_data)


def persist_card(card, context):
    # due date and completion status
    if "planka_due_date" in card and "planka_is_due_date_completed" in card:
        due_date = timestamp_format(card['planka_due_date'], timezone=True)
        is_due_date_completed = card['planka_is_due_date_completed']
    else:
        due_date = None
        is_due_date_completed = None

    # archived card TODO: add metadata by using json snippet
    list_id = card['planka_list_id']
    if card.get("planka_card_is_archived") is True:
        list_id = card['planka_archive_list_id']
        card['title'] = '[Архив] ' + card['title']  # card title prefix

    # CARD
    instance = Card(
        board_id=card['planka_board_id'],
        list_id=list_id,
        creator_user_id=card['planka_creator_user_id'],
        position="1000",
        name=card['title'],
        description=html_to_markdown(card['description']),
        is_due_date_completed=is_due_date_completed,
        due_date=due_date,
        created_at=timestamp_format(card['timestamp'], timezone=True)
    )
    unique_keys = {
        'board_id': instance.board_id,
        'list_id': instance.list_id,
        'created_at': instance.created_at,
        'name': instance.name
    }
    created_card_instance = persist(instance, unique_keys, context=context)
    print(f"  Added card "
          f"{card['id']} / {created_card_instance.id}")
    
    # attachment
    # identify_attachments(
    #     card['description'],
    #     context,
    #     created_card_instance.id
    # )

    # card label
    if "planka_card_label" in card:
        for label in card["planka_card_label"]:
            created_label_instance = persist_label(label, context)
            persist_card_label(
                created_label_instance.id,
                instance.id,
                instance.created_at,
                context
            )

    # card membership
    if "planka_card_membership" in card:
        for member in card["planka_card_membership"]:
            persist_card_membership(member, instance.id, context)

    # actions (chat)
    if "planka_action" in card:
        for action in card['planka_action']:
            persist_action(action, instance.id, context)

    # tasks (checklists)
    if "planka_task" in card:
        position = 65535
        for task in card['planka_task']:
            persist_task(
                task,
                card_id=instance.id,
                created_at=instance.created_at,
                position=position,
                context=context
            )
            position += 65535

    # recursion for subcards
    if card.get('data', {}).get('subtaskList', {}).get('subtasks'):
        for subcard in card['data']['subtaskList']['subtasks']:
            persist_card(subcard, context)


if __name__ == "__main__":
    card_data = load_json('task.json')
    if not card_data:
        raise TypeError("File task.json doesn't exist or empty!")

    # target_card = '152a60cf-bfb7-40ec-917d-d5000b687917'
    # target_card = '953096e4-7f0a-4a30-9659-40115bea507d'
    target_card = 'eb79b211-0b17-4d09-bac8-c12c2ae43aaa'
    card = next(
        (obj for obj in card_data if obj.get('id') == target_card),
        None
    )
    context = TransactionContext()
    try:
        persist_card(card, context)
        print("Done! To revert changes in "
              "the database, use service.undo")
    except Exception as e:
        print(f"Error processing card {card["id"]}: {e}")
    finally:
        save_transaction_log(context)
