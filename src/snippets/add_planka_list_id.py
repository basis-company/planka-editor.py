'''
Переносит list_id в task.json для оптимизации импорта карточек
'''

from src.services.data import load_json, save_json


def add_planka_list_id():
    tasks = load_json('task.json')
    lists = load_json('list.json')

    list_map = {
        list_item['id']: list_item['planka_id'] for list_item in lists if 'id' in list_item and 'planka_id' in list_item
    }

    for task in tasks:
        if 'location' in task:
            location_id = task['location']
            planka_list_id = list_map.get(location_id)
            if planka_list_id:
                task['planka_list_id'] = planka_list_id

    save_json('task.json', tasks)


add_planka_list_id()
