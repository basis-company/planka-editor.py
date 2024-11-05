"""
Итерация 4: Импортируем списки на доски.
"""

from datetime import datetime
from src.models.list import List

from src.crud import persist
from src.services.data import load_json, save_json
from src.services.location import get_location_planka_id


# Тайтлы стикеров, которые будут игнорироваться
FORBIDDEN_TITLES = ['User', 'Deadline']

list_data = load_json('list.json')


# Lists
for list_entity in list_data:
    list_instance = List(
        board_id=get_location_planka_id('board.json', list_entity['location']),
        name=list_entity['title'],
        created_at=datetime.fromtimestamp(
            list_entity['timestamp'] / 1000
        ),
        position=list_entity['data']['columnColor']['hue'] * 10
    )

    created_list_data = persist(
        list_instance, 
        {   # unique keys
            'name': list_instance.name,
            'board_id': list_instance.board_id
        }
    )

    if created_list_data is None:
        print(f'Лист {list_entity["title"]} '
                'является дублем и не будет создан!')
        continue
    else:
        print(f"Лист {list_instance.name} создан на "
                f"доске {list_instance.board_id}.")
        list_entity['planka_id'] = created_list_data.id


save_json('list.json', list_data)
print('Готово. Импорт успешно завершен. '
      'Идентификаторы Planka добавлены в json. '
      'Для отмены импорта воспользуйтесь сервисом undo.py')
