from src.services.data import load_json
from src.services.data import save_json

def split_tasks_by_subtask():
    task_data = load_json('task.json')

    tasks_without_subtasks = []
    tasks_with_subtasks = []

    for task in task_data:
        if 'data' in task and 'subtaskList' in task['data']:
            tasks_with_subtasks.append(task)
        else:
            tasks_without_subtasks.append(task)

    try:
        save_json('task_single.json', tasks_without_subtasks)
        save_json('task_parent.json', tasks_with_subtasks)
    except Exception as e:
        print(f"Ошибка при записи в файлы: {e}")

split_tasks_by_subtask()
