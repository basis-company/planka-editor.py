from src.services.data import load_json, save_json


def remove_stickers_recursive(task):
    """Рекурсивно удаляет ключ stickers из карточек."""
    if "stickers" in task:
        del task["stickers"]

    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtasks:
        remove_stickers_recursive(subtask)


def main(tasks_file):
    """Открывает файл с тасками и удаляет stickers из карточек."""
    tasks = load_json(tasks_file)

    for task in tasks:
        remove_stickers_recursive(task)

    save_json(tasks_file, tasks)
    print(f'[main] Done!')


main("task.json")
