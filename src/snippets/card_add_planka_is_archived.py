'''
Добавляем ключ указывающий на то что карточка архивирована.
'''
from src.services.data import load_json, save_json


def mark_archived_tasks(task, archived_ids):
    task_id = task.get("id")
    task["planka_card_is_archived"] = task_id in archived_ids

    # Recursion for subtasks
    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    if isinstance(subtasks, list):
        for subtask in subtasks:
            mark_archived_tasks(subtask, archived_ids)


def main():
    tasks = load_json("task.json")
    archived_ids = load_json("archived_cards.json")

    for task in tasks:
        mark_archived_tasks(task, archived_ids)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
