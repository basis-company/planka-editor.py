from src.services.data import load_json, save_json


def ensure_description(task):
    """
    Рекурсивно добавляет ключ 'description' с пустым значением
    всем задачам, у которых этот ключ отсутствует.
    Работает рекурсивно для обработки вложенных карточек.
    """
    if 'description' not in task:
        task['description'] = ""
        print(f"Task with id {task['id']} was missing a description")

    # for subcards
    subtask_list = (
        task.get('data', {})
        .get('subtaskList', {})
        .get('subtasks', [])
    )
    for subtask in subtask_list:
        ensure_description(subtask)


def process_tasks(file_name):
    """
    Загружает задачи из файла, добавляет отсутствующие
    ключи 'description', сохраняет изменения.
    """
    tasks = load_json(file_name)

    for task in tasks:
        ensure_description(task)

    save_json(file_name, tasks)


if __name__ == "__main__":
    process_tasks("task.json")
