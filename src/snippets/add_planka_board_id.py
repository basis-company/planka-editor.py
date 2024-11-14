'''
Переносит board_id в task.json для оптимизации импорта карточек
'''
from src.services.data import load_json, save_json


def add_planka_board_id():
    tasks = load_json('task.json')
    lists = load_json('list.json')
    boards = load_json('board.json')

    list_location_map = {
        list_item['id']: list_item['location'] for list_item in lists if 'id' in list_item and 'location' in list_item
    }

    board_planka_id_map = {
        board['id']: board['planka_id'] for board in boards if 'id' in board and 'planka_id' in board
    }

    for task in tasks:
        if 'location' in task:
            initial_location = task['location']

            intermediate_location = list_location_map.get(initial_location)

            if intermediate_location:
                planka_board_id = board_planka_id_map.get(intermediate_location)

                if planka_board_id:
                    task['planka_board_id'] = planka_board_id

    save_json('task.json', tasks)


add_planka_board_id()
