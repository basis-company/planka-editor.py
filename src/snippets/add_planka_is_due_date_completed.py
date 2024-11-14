'''
Переносит is_due_date_completed в task.json для оптимизации импорта карточек
и чистит данные от лишних ключей.
'''
from src.services.data import load_json, save_json


def add_planka_is_due_date_completed():
    tasks = load_json('task.json')

    for task in tasks:
        if 'data' in task and 'gtd' in task['data'] and 'state' in task['data']['gtd']:
            gtd_stage = task['data']['gtd']['state'].get('stage')

            if gtd_stage == 'done':
                task['planka_is_due_date_completed'] = True

            del task['data']['gtd']

    save_json('task.json', tasks)


add_planka_is_due_date_completed()
