"""
Сниппет считает кол-во подзадач (subtasks), для оценки и проверки наличия в subtask.json, а также проверяет location.
"""

from src.services.data import load_json


def subtasks_count():
    task_data = load_json('task.json')
    subtask_data = load_json('subtask.json')

    result_count = 0
    unique_subtasks = set() # Для учета уникальных подзадач из task.json
    found_in_subtask = set() # Для подзадач, найденных в subtask.json
    missing_in_subtask = [] # Для подзадач, отсутствующих в subtask.json

    subtask_ids = {subtask['id'] for subtask in subtask_data}

    task_ids = {task_entity['id'] for task_entity in task_data}

    try:
        for task_entity in task_data:
            subtasks_dict = task_entity.get('data', {}).get('subtaskList', {}).get('subtasks')
            if isinstance(subtasks_dict, dict):
                result_count += len(subtasks_dict)
                unique_subtasks.update(subtasks_dict.keys())

                for subtask_id in subtasks_dict.keys():
                    if subtask_id in subtask_ids:
                        found_in_subtask.add(subtask_id)
                    else:
                        missing_in_subtask.append(subtask_id)

        extra_in_subtask = subtask_ids - unique_subtasks

        location_report = {}
        for extra_id in extra_in_subtask:
            extra_subtask = next((
                st for st in subtask_data if st['id'] == extra_id
            ), None)
            if extra_subtask:
                location = extra_subtask.get('location')
                if location in task_ids:
                    location_report[extra_id] = f"Location '{location}' найден в task.json"
                else:
                    location_report[extra_id] = f"Location '{location}' НЕ найден в task.json"

    except Exception as e:
        print('Ошибка при обработке данных: ', str(e))

    # result
    print(f'Кол-во SubTasks внутри Tasks: {result_count}')
    print(f'Кол-во уникальных SubTasks: {len(unique_subtasks)}')
    print(f'Найдено в subtask.json: {len(found_in_subtask)}')
    print(f'Не найдено в subtask.json: {len(missing_in_subtask)}')

    print('Список не найденных сабтасков в subtask.json:')
    for subtask_id in missing_in_subtask:
        print(subtask_id)

    print('Список лишних сабтасков из subtask.json:')
    for extra_id in extra_in_subtask:
        print(extra_id)

    print("Отчёт по проверке location для лишних сабтасков из subtask.json:")
    for subtask_id, report in location_report.items():
        print(f"id: {subtask_id}, {report}")


subtasks_count()
