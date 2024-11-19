'''
Сниппет строит иерархию task/subtask для корректного
импорта карточек с сохранением связей.
'''
from src.services.data import load_json, save_json


def main(file_name):
    tasks = load_json(file_name)

    tasks_to_keep = []
    tasks_by_id = {task["id"]: task for task in tasks}

    for task in tasks:
        subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks")
        if subtasks:
            for subtask_id in list(subtasks.keys()):
                subtask = tasks_by_id.get(subtask_id)
                if subtask:
                    subtasks[subtask_id] = subtask

            tasks_by_id = {
                key: value for key, value in tasks_by_id.items() if key not in subtasks.keys()
            }

    tasks_to_keep = list(tasks_by_id.values())

    save_json(file_name, tasks_to_keep)
    print("Done!")


main("task.json")
