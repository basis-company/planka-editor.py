from typing import Dict
from markdownify import MarkdownConverter
from sqlalchemy.orm import Session

from src.models.card import Card
from src.models.transaction import TransactionContext
from src.models.metadata import Metadata

from src.crud import persist, database
from src.services.data import load_json, save_json
from src.services.timestamp import timestamp_format

from src.importers.label import persist_label
from src.importers.card_label import persist_card_label
from src.importers.card_membership import persist_card_membership
from src.importers.task import persist_task
from src.importers.action import persist_action

from constants import TASK_FILE_NAME


def persist_card(
    card,
    context: TransactionContext,
    parent_data: Dict[str, any] = None,
    session: Session = None
):
    try:
        # due date and completion status
        if (
            "planka_due_date" in card and
            "planka_is_due_date_completed" in card
        ):
            due_date = timestamp_format(card['planka_due_date'], timezone=True)
            is_due_date_completed = card['planka_is_due_date_completed']
        else:
            due_date = None
            is_due_date_completed = None

        # card metadata
        metadata = Metadata()

        # archived card
        list_id = card['planka_list_id']
        if card.get("planka_card_is_archived") is True:
            list_id = card['planka_archive_list_id']
            card['title'] = '[Архив] ' + card['title']  # card title prefix
            metadata.add_metadata_row(
                f"archived_from_board: {card['planka_list_id']}"
            )
            metadata.add_metadata_row(
                f"archived_from_list: {card['planka_board_id']}"
            )

        # parent card data
        if (
            card.get("data", {})
            .get("subtaskList", {})
            .get("subtasks")
            is not None
        ):
            # TODO: add metadata for parents
            card['title'] = "❖ " + card['title']  # card title prefix
        if parent_data:
            metadata.add_parent(parent=parent_data)  # link to the parent card
            card['title'] = "– " + card['title']

        # card
        description = MarkdownConverter().convert(
            card['description']
        )
        description = (
            description.replace("\\.", ".")
            .replace("\\-", "-")
            .replace("\\#", "#")
        )
        description = metadata.get() + description
        instance = Card(
            board_id=card['planka_board_id'],
            list_id=list_id,
            creator_user_id=card['planka_creator_user_id'],
            position=65535,
            name=card['title'],
            description=description,
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
        card_instance = persist(
            instance=instance,
            unique_keys=unique_keys,
            session=session,
            context=context
        )
        print(f"  Card "
              f"{card['id']} / {card_instance.id} "
              f"added")

        # card label
        if "planka_card_label" in card:
            for label in card["planka_card_label"]:
                created_label_instance = persist_label(
                    label=label,
                    session=session,
                    context=context
                )
                persist_card_label(
                    label_id=created_label_instance.id,
                    card_id=instance.id,
                    created_at=instance.created_at,
                    session=session,
                    context=context
                )

        # card membership
        if "planka_card_membership" in card:
            for member in card["planka_card_membership"]:
                persist_card_membership(
                    member=member,
                    card_id=instance.id,
                    session=session,
                    context=context
                )

        # actions (chat)
        if "planka_action" in card:
            for action in card['planka_action']:
                persist_action(
                    action=action,
                    card_id=instance.id,
                    session=session,
                    context=context
                )

        # tasks (checklists)
        if "planka_task" in card:
            position = 65535
            for task in card['planka_task']:
                persist_task(
                    task=task,
                    card_id=instance.id,
                    created_at=instance.created_at,
                    position=position,
                    session=session,
                    context=context
                )
                position += 65535

        # subcards recursion
        if card.get('data', {}).get('subtaskList', {}).get('subtasks'):
            for subcard in card['data']['subtaskList']['subtasks']:
                parent = {
                    "id": instance.id,
                    "name": instance.name
                }
                persist_card(
                    card=subcard,
                    context=context,
                    parent_data=parent,
                    session=session
                )

        return card_instance

    except Exception as e:
        print(f"Error processing card {card["id"]}: {e}")


def main(card_ids):
    card_data = load_json(TASK_FILE_NAME)
    if not card_data:
        raise TypeError(f"[Error] File {TASK_FILE_NAME} "
                        f"doesn't exist or empty!")

    context = TransactionContext()  # cards to persist

    with database() as session:
        try:
            planka_keys = []  # persisted card ID's 

            for card_id in card_ids:
                card = next(
                    (obj for obj in card_data if obj.get('id') == card_id),
                    None
                )
                if card:
                    created_card = persist_card(
                        card=card,
                        context=context,
                        session=session
                    )
                    planka_keys.append(
                        {
                            "id": card["id"],
                            "planka_id": created_card.id
                        }
                    )
                else:
                    print(f"[Warning] ID {card_id} wasn't "
                          f"found in {TASK_FILE_NAME}!")

            session.commit()
            context.commit()

            # adding planka_keys to task.json
            for card in card_data:
                if card['id'] in planka_keys:
                    card['planka_id'] = planka_keys[card['id']]
            save_json("task.json", card_data)

        except Exception as e:  # TODO: fix exception handler 
            session.rollback()
            context.rollback()
            print(f"[Error] Processing Card {card["id"]}: {e}\n")


if __name__ == "__main__":
    card_ids = [
        '2c30aa5b-b65a-4ae3-854b-1279f0d187cc'#,  # много субкарт
        # '152a60cf-bfb7-40ec-917d-d5000b687917',
        # '953096e4-7f0a-4a30-9659-40115bea507d',
        # 'bbd599a8-36dd-4ba4-a95c-4025c356ba56',  # много тасков
        # 'fe014e60-5424-4ab1-b90e-3f60ca1bffd4',  # у субкарты в комментах есть url на другую карту
        # '5cc9d10d-ce0a-497d-b78f-d80753ffcff2'  # у карты есть вложение нестандартного формата
    ]
    main(card_ids)
