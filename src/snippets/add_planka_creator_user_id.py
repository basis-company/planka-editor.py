'''
Переносит user_id в task.json для оптимизации импорта карточек
'''
from src.services.data import load_json, save_json


def add_planka_creator_user_id():
    tasks = load_json('task.json')
    users = load_json('user.json')

    user_map = {
        user['id']: user['planka_id'] for user in users if 'id' in user and 'planka_id' in user
    }

    for task in tasks:
        if 'data' in task and 'by' in task['data']:
            user_id = task['data']['by']
            planka_creator_id = user_map.get(user_id)
            if planka_creator_id:
                task['planka_creator_user_id'] = planka_creator_id

    save_json('task.json', tasks)


add_planka_creator_user_id()
