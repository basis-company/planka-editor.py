from src.services.data import load_json, save_json


# Функция для получения уникальных комбинаций сообщений
def extract_unique_message_types():
    data = load_json("task.json")
    unique_combinations = {}

    # Получаем все сообщения внутри chat.messages
    messages = data.get("chat", {}).get("messages", {})

    for timestamp, message in messages.items():
        msg_type = message.get("dataType")
        from_system = message.get("properties", {}).get("fromSystem", False)
        move_action = message.get("properties", {}).get("move", False)

        # Ключ комбинации на основе уникальных признаков
        combination_key = f"{msg_type}_{from_system}_{move_action}"

        # Сохраняем пример сообщения для каждой комбинации
        if combination_key not in unique_combinations:
            unique_combinations[combination_key] = {
                "timestamp": timestamp,
                "id": message.get("id"),
                "dataType": msg_type,
                "properties": message.get("properties", {}),
                "text": message.get("text", "")
            }

    save_json("messages_types.json", unique_combinations)


# Пример вызова функции
extract_unique_message_types()
