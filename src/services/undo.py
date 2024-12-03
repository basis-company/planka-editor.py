from src.crud import erase
from src.services.data import load_json, save_json
from src.services.upload import remove_attachment

from constants import LOG_FILE_NAME
from constants import ENTITY_TYPES


# deprecated method
def undo_per_types(entity_class_name: str):
    """Метод для отмены загрузки сущностей определенного класса."""
    uploaded_data = load_json("log_old.json")

    if entity_class_name not in uploaded_data:
        print(f"Нет данных для удаления по типу {entity_class_name}.")
        return

    entity_class = ENTITY_TYPES.get(entity_class_name)
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

    save_json("log_old.json", uploaded_data)
    print(f"Отмена завершена для всех {entity_class_name}. Ключ "
          f"{entity_class_name} удалён из log_old.json")


# recommended method
def undo_transaction(transaction_id: str):
    """Метод для отмены загрузки по id транзакции."""
    uploaded_data = load_json(LOG_FILE_NAME)
    if not uploaded_data or transaction_id not in uploaded_data:
        print(f"[Error] Transaction {transaction_id} "
              f"is missing from {LOG_FILE_NAME}")
        return

    entities = uploaded_data[transaction_id]
    remaining_entities = []  # keep in transactions.json

    for entity in entities:
        entity_class = ENTITY_TYPES.get(entity["type"])
        if entity_class is None:
            print(f"    Entity type {entity['type']} not found.")
            remaining_entities.append(entity)
            continue
        elif entity_class == 'Attachment':
            if remove_attachment(entity['id']):
                print(f"    {entity['type']} {entity['id']} removed...")
            else:
                print(f"[Warning] {entity['type']}: {entity['id']} not removed "
                      f"for some reason and will be kept in {LOG_FILE_NAME}!")
                remaining_entities.append(entity)
        else:
            if erase(entity_class, entity["id"]):
                print(f"    {entity['type']} {entity['id']} removed...")
            else:
                print(f"[Warning] {entity['type']}: {entity['id']} not removed "
                      f"for some reason and will be kept in {LOG_FILE_NAME}!")
                remaining_entities.append(entity)

    if remaining_entities:
        print(f"[Warning] Failed to remove one or more entities "
              f"from transaction {transaction_id}.")
        uploaded_data[transaction_id] = remaining_entities
    else:
        print(f"  All entities from transaction "
              f"{transaction_id} was successfully removed.")
        del uploaded_data[transaction_id]

    save_json(LOG_FILE_NAME, uploaded_data)


if __name__ == "__main__":
    undo_transaction('1733246673166')
    print(f"Done! File {LOG_FILE_NAME} was updated.")
