'''
Сниппет подсчитывает кол-во типов сообщений на основании различных
комбинаций ключей и выводит примеры для каждого типа.
'''

from src.services.data import load_json, save_json


def get_keys_recursive(data, parent_key=""):
    """
    Рекурсивно собирает все ключи из объекта, включая вложенные уровни.

    Args:
        data (dict): Исходный объект для анализа.
        parent_key (str): Префикс для ключей на текущем уровне вложенности.

    Returns:
        set: Набор ключей, включая все вложенные.
    """
    keys = set()

    for key, value in data.items():
        full_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            keys.update(get_keys_recursive(value, full_key))
        else:
            keys.add(full_key)

    return keys


def extract_message_types():
    tasks = load_json("task.json")

    unique_types = {}
    example_counter = 1

    for task in tasks:
        chat_messages = task.get("chat", {}).get("messages", {})

        for timestamp, message_data in chat_messages.items():

            key_set = frozenset(get_keys_recursive(message_data))

            if key_set not in unique_types:
                unique_types[key_set] = {
                    "example_id": example_counter,
                    "message_data": message_data
                }
                example_counter += 1

    output_data = {
        str(info["example_id"]): info["message_data"] for info in unique_types.values()
    }

    save_json("_message_types.json", output_data)
    print("Уникальные типы сообщений успешно сохранены в messages_types.json")


if __name__ == "__main__":
    extract_message_types()
