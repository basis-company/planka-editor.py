import re
from datetime import datetime
from src.models.card import Card

from src.crud import persist
from src.services.upload import persist_attachment
from src.importers.label import persist_label
from src.importers.card_label import persist_card_label
from src.importers.card_membership import persist_card_membership
from src.importers.task import persist_task
from src.importers.action import persist_action

from src.services.data import load_json
''' TODO:
[+] Card entity
    [+] due date and completion status
    [+] archived card placement logic
[+] CardLabel connection + persist Labels
[+] CardMembership entities
[+] Action entities (chat messages)
[+] Task entities (checklists)
[ ] Add recursion for subtask
[ ] Add metadata to subtasks description and title (snippet)
'''


'''TEMP'''
target_card = '152a60cf-bfb7-40ec-917d-d5000b687917'

card_data = load_json('task.json')
if not card_data:
    raise TypeError('Файл task.json не найден или пуст!')

# target card
card = next((obj for obj in card_data if obj.get('id') == target_card), None)


def identify_attachments(card):
    description = card.get('planka_description', '')

    # regex for extracting url's from description
    url_pattern = re.compile(r'https?://[^\s]+')
    links = url_pattern.findall(description)

    if not links:
        print("[identify_attachments] Вложения не обнаружены.")
        return description

    for link in links:
        if "yougile.com" in link:
            # print(f"[identify_attachments] Найдена ссылка на YouGile: {link}")
            attachment = persist_attachment(link, card['id'])
            if attachment:
                new_url = (
                    f"https://planka.basis.services/"
                    f"attachments/{attachment['attachment_id']}/"
                    f"download/{attachment['filename']}"
                )
                print(f"[identify_attachments] Добавлено вложение: {new_url}")
                description = description.replace(link, new_url)

    return description


# CARD
def persist_card(card):
    # due date and completion status
    if "planka_due_date" in card and "planka_is_due_date_completed" in card:
        due_date = datetime.fromtimestamp(card['planka_due_date'] / 1000)
        is_due_date_completed = card['planka_is_due_date_completed']
    else:
        due_date = None
        is_due_date_completed = None

    # archived card
    list_id = card['planka_list_id']
    if card.get("planka_card_is_archived") is True:
        list_id = card['planka_archive_list_id']
        card['title'] = '[Архив] ' + card['title']  # card title prefix

    instance = Card(
        board_id=card['planka_board_id'],
        list_id=list_id,
        creator_user_id=card['planka_creator_user_id'],
        position="1000",  # TODO: calculation logic
        name=card['title'],
        description=identify_attachments(card),
        is_due_date_complete=is_due_date_completed,
        due_date=due_date,
        created_at=datetime.fromtimestamp(card['timestamp'] / 1000)
    )
    unique_keys = {
        'board_id': instance.board_id,
        'list_id': instance.list_id,
        'created_at': instance.created_at,
        'name': instance.name
    }
    created_card_instance = persist(instance, unique_keys)
    print(f'[persist_card] Добавлена карточка '
          f'{card['id']} / {created_card_instance.id}')

    # card label
    if "planka_card_label" in card:
        for label in card["planka_card_label"]:
            created_label_instance = persist_label(label)
            persist_card_label(
                created_label_instance.id,
                created_card_instance.id,
                created_card_instance.created_at
            )

    # card membership
    if "planka_card_membership" in card:
        for member in card["planka_card_membership"]:
            persist_card_membership(member, created_label_instance.id)

    # actions (chat)
    if "planka_action" in card:
        for action in card['planka_action']:
            persist_action(action, created_card_instance.id)

    # tasks (checklists)
    if "planka_task" in card:
        for task in card['planka_task']:
            persist_task(
                task,
                created_card_instance.id,
                created_card_instance.created_at
            )

    # recursion for subcards
    if card.get('data', {}).get('subtaskList', {}).get('subtasks'):
        # print("[persist_card] Обнаружены вложенные карточки")
        for subcard in card['data']['subtaskList']['subtasks']:
            persist_card(subcard)

    # recursion for subcards
    if "data" in task and "subtaskList" in task["data"]:
        for subcard in task["data"]["subtaskList"].get("subtasks", []):
            persist_card(subcard)

    return created_card_instance


if __name__ == "__main__":
    persist_card(card)
