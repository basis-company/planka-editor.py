from src.services.data import load_json, save_json


def find_create_at(label_id, labels):
    """Ищет дату создания лейбла в массиве labels."""
    for label in labels:
        if label["id"] == label_id:
            return label['timestamp']


def find_label_state(label_id, state_key, labels):
    """Ищет состояние лейбла в массиве labels."""
    for label in labels:
        if label["id"] == label_id:
            states = label.get("states", {}).get("index", {})
            return states.get(state_key)
    return None


def process_task(task, labels):
    """Рекурсивная обработка карточек."""
    planka_card_labels = []

    stickers = task.get("stickers", {})
    for label_id, state_key in stickers.items():
        state_key = state_key or "blank"  # Если пустая строка, ищем ключ blank
        state = find_label_state(label_id, state_key, labels)
        if state:
            planka_card_labels.append({
                # "id": state.get("id", ""),
                "board_id": task.get("planka_board_id", ""),
                "name": state.get("name", ""),
                # "color": state.get("color", ""),
                "color": state.get("planka_color", ""),
                "created_at": find_create_at(label_id, labels)
            })
        else:
            print(f'[process_task] Не найдено состояние {state_key} для лейбла {label_id}')

    if planka_card_labels:
        task["planka_card_label"] = planka_card_labels

    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtasks:
        process_task(subtask, labels)


def main(tasks_file, labels_file):
    tasks = load_json(tasks_file)
    labels = load_json(labels_file)

    for task in tasks:
        process_task(task, labels)

    save_json(tasks_file, tasks)
    print('[main] Done!')


main("task.json", "label.json")
