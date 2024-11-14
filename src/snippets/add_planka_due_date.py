'''
Переносит due_date в task.json для оптимизации импорта карточек
'''
from src.services.data import load_json, save_json


def add_planka_due_date():
    tasks = load_json('task.json')
    sticker_id = "00050d5a-64a9-49a6-8bec-f883d8909173"

    for task in tasks:
        if 'stickers' in task and sticker_id in task['stickers']:
            sticker_data = task['stickers'][sticker_id]

            if 'current' in sticker_data and 'deadline' in sticker_data['current']:
                task['planka_due_date'] = sticker_data['current']['deadline']

            del task['stickers'][sticker_id]

            if not task['stickers']:
                del task['stickers']

    save_json('task.json', tasks)


add_planka_due_date()
