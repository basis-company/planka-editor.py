from datetime import datetime
from src.models.card_label import CardLabel
from src.models.card_membership import CardMembership
from src.models.action import Action
from src.models.task import Task
from src.models.card import Card

from src.crud import persist
from src.services.data import load_json, save_json
from src.services.markdown2 import html_to_markdown
'''
LOGIC:
1.  Card entity (description already updated with markdown2)
    Attachments if description has attachments links
2.  CardLabel connection. If they are not there then persist Label
    TODO: Update persist method to return the entity of the duplicate
3.  CardMembership entities
4.  Action entities (chat messages)
5.  Task entities (checklists)
'''


target_card = '602e87fd-d072-4020-abb9-190b3ab7784f'  # tmp

card_data = load_json('task.json')
if not card_data:
    raise TypeError('Файл task.json не найден или пуст!')

# target card
card = next((obj for obj in card_data if obj.get('id') == target_card), None)


# CARD
def persist_card(card):
    # due date and completion status
    if "planka_due_date" in card and "planka_is_due_date_completed" in card:
        due_date = datetime.fromtimestamp(card['planka_due_date'] / 1000)
        is_due_date_completed = card['planka_is_due_date_completed']
    else:
        due_date = None
        is_due_date_completed = None

    # is card archived
    if card.get("planka_card_is_archived") is True:
        card['title'] = '[АРХИВ] ' + card['title']

    instance = Card(
        board_id=card['planka_board_id'],
        list_id=card('planka_list_id'),
        creator_user_id=card['planka_creator_user_id'],
        position='16000',  # TODO: need calculation logic
        name=card['title'],
        description=html_to_markdown(card['description']),
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
    created_instance = persist(instance, unique_keys)

    # recursion for subcards
    if card.get('data', {}).get('subtaskList', {}).get('subtasks'):
        print("[persist_card] Обнаружены вложенные карточки")
        for subcard in card['data']['subtaskList']['subtasks']:
            # подготовка ссылок на родительскую карточку
            persist_card(subcard)

    return created_instance
