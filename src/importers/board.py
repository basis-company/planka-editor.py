"""
Итерация 2: Импортер для уровня досок.
"""

from datetime import datetime
from src.models.board import Board

from src.crud import persist
from src.services.location import get_location_planka_id
from src.services.data import load_json, save_json


board_data = load_json('board.json')
if not board_data:
    print('Файл board.json не найден или пуст!')
    board_data = []


# Boards
for board_entity in board_data:    
    board_instance = Board(
        name=board_entity['title'],
        project_id=get_location_planka_id(
            'project.json',
            board_entity['location']
        ),
        created_at=datetime.fromtimestamp(board_entity['timestamp'] / 1000),
        position=0
    )

    unique_keys = {
        'name': board_instance.name,
        'project_id': board_instance.project_id
    }
    created_project_data = persist(board_instance, unique_keys)

    if created_project_data is None:
        print(f'Доска {board_entity["title"]} '
              f'является дублем и не будет создана!')
        continue
    else:
        print(f'Доска {board_entity["title"]} создана.')
        board_entity['planka_id'] = created_project_data.id


# Update projects.json
save_json('board.json', board_data)
print('Доски успешно импортированы в проекты Planka. '
      'Данные сохранены в board.json')
