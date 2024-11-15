from src.crud import erase
from src.services.data import load_json, save_json

from constants import LOG_FILE_NAME

from src.models.label import Label
from src.models.action import Action
from src.models.board import Board
from src.models.card import Card
from src.models.project_manager import ProjectManager
from src.models.project import Project
from src.models.user_account import UserAccount


class_mapping = {
    'Label': Label,
    'Action': Action,
    'Board': Board,
    'Card': Card,
    'ProjectManager': ProjectManager,
    'Project': Project,
    'UserAccount': UserAccount
}


def undo(entity_class_name: str):
    uploaded_data = load_json(LOG_FILE_NAME)

    if entity_class_name not in uploaded_data:
        print(f"Нет данных для удаления по типу {entity_class_name}.")
        return

    entity_class = class_mapping.get(entity_class_name)
    if entity_class is None:
        print(f"Класс сущности {entity_class_name} не найден.")
        return

    entity_ids = uploaded_data[entity_class_name]
    remaining_ids = []

    for entity_id in entity_ids:
        if erase(entity_class, entity_id):
            print(f"Удалено: {entity_class_name} с ID {entity_id}.")
        else:
            print(f"Сущность {entity_class_name} с ID {entity_id} "
                  "не найдена и не будет удалена.")
            remaining_ids.append(entity_id)

    if remaining_ids:
        uploaded_data[entity_class_name] = remaining_ids
    else:
        del uploaded_data[entity_class_name]

    save_json(LOG_FILE_NAME, uploaded_data)
    print(f"Отмена завершена для всех {entity_class_name}. Ключ "
          f"{entity_class_name} удалён из {LOG_FILE_NAME}")
