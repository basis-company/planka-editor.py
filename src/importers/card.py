import re
from datetime import datetime

from constants import LOG_FILE_NAME

from src.models.card import Card
from src.models.transaction import TransactionContext

from src.crud import persist, database
from src.services.data import load_json, save_json

from src.importers.label import persist_label
from src.importers.card_label import persist_card_label
from src.importers.card_membership import persist_card_membership
from src.importers.task import persist_task
from src.importers.action import persist_action
from src.services.upload import persist_attachment


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
    uploaded_data[context.transaction_id] = {
        "timestamp": transaction_data["timestamp"],
        "entities": transaction_data["entities"]
    }
    save_json(LOG_FILE_NAME, uploaded_data)


def update_card_description(card_id: int, text: str) -> None:
    """Обновляет описание карточки в базе."""
    with database() as session:
        card_instance = session.query(Card).get(card_id)
        if not card_instance:
            raise LookupError(f"Card with id {card_id} not found!")
        card_instance.description = text
        session.commit()

    print(f"[update_card_description] Card {card_id} "
          f"description was successfully updated.")


def identify_attachments(text, context, card_id=None):
    """Находит в тексте ссылки на файлы, создает вложения на их
    основе и заменяет ссылки в тексте на актуальные planka url."""
    # regex patterns
    url_pattern = re.compile(r'https?://[^\s)]+')
    file_pattern = re.compile(r"/root/#file:/user-data/([a-f0-9-]+)/(.+)")

    links = url_pattern.findall(text)
    if not links:
        return text

    # external yougile file links
    for link in links:
        if "yougile.com" in link:
            print(f"[identify_attachments] YouGile URL found: {link}")
            attachment = persist_attachment(link, card_id, context)
            if attachment:
                new_url = (
                    f"https://planka.basis.services/"
                    f"attachments/{attachment['id']}/"
                    f"download/{attachment['name']}"
                )
                print(f"[identify_attachments] Attachment added: {new_url}")
                text = text.replace(link, new_url)

    # internal yougile file links
    file_matches = file_pattern.findall(text)
    for file_id, file_name in file_matches:
        new_file_url = (
            f"https://ru.yougile.com/user-data/"
            f"{file_id}/"
            f"{file_name}"
        )
        print(f"[identify_attachments] Attachment added: {new_file_url}")
        attachment = persist_attachment(new_file_url, card_id, context)
        if attachment:
            text = text.replace(f"/root/#file:/user-data/"
                                f"{file_id}/{file_name}", new_file_url)

    if card_id:
        update_card_description(card_id, text)

    return text


def persist_card(card, context):
    # due date and completion status
    if "planka_due_date" in card and "planka_is_due_date_completed" in card:
        due_date = datetime.fromtimestamp(card['planka_due_date'] / 1000)
        is_due_date_completed = card['planka_is_due_date_completed']
    else:
        due_date = None
        is_due_date_completed = None

    # archived card TODO: json snippet
    list_id = card['planka_list_id']
    if card.get("planka_card_is_archived") is True:
        list_id = card['planka_archive_list_id']
        card['title'] = '[Архив] ' + card['title']  # card title prefix

    # CARD
    instance = Card(
        board_id=card['planka_board_id'],
        list_id=list_id,
        creator_user_id=card['planka_creator_user_id'],
        position="1000",  # TODO: calculation logic
        name=card['title'],
        description=card['description'],
        is_due_date_completed=is_due_date_completed,
        due_date=due_date,
        created_at=datetime.fromtimestamp(card['timestamp'] / 1000)
    )
    unique_keys = {
        'board_id': instance.board_id,
        'list_id': instance.list_id,
        'created_at': instance.created_at,
        'name': instance.name
    }
    created_card_instance = persist(instance, unique_keys, context=context)
    print(f"[persist_card] Added card "
          f"{card['id']} / {created_card_instance.id}")
    identify_attachments(card['description'], context,
                         created_card_instance.id)

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
        for task in card['planka_task']:
            persist_task(
                task,
                instance.id,
                instance.created_at,
                context
            )

    # recursion for subcards
    if card.get('data', {}).get('subtaskList', {}).get('subtasks'):
        for subcard in card['data']['subtaskList']['subtasks']:
            persist_card(subcard, context)


if __name__ == "__main__":
    card_data = load_json('task.json')
    if not card_data:
        raise TypeError("File task.json doesn't exist or empty!")

    target_card = '152a60cf-bfb7-40ec-917d-d5000b687917'  # temp target card
    card = next(
        (obj for obj in card_data if obj.get('id') == target_card),
        None
    )
    context = TransactionContext()
    try:
        persist_card(card, context)
    except Exception as e:
        print(f"Error processing card {card["id"]}: {e}")
    finally:
        save_transaction_log(context)
        print("[service.card] Done! To revert changes in "
              "the database, use service.undo")
