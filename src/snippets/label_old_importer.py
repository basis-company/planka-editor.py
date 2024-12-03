"""
Итерация 3: Импортируем метки на доски.
"""

from datetime import datetime
from src.models.label import Label

from src.crud import persist
from src.services.data import load_json, save_json
from src.services.timestamp import timestamp_format


# Тайтлы стикеров, которые будут игнорироваться
FORBIDDEN_TITLES = ['User', 'Deadline']

board_data = load_json('board.json')
label_data = load_json('label.json')


# Boards
for board_entity in board_data:
    if 'stickers' not in board_entity:
        continue
    else:
        board_labels = list(board_entity['stickers'].keys())
        position_iterator = 50

        # Labels
        for label_id in board_labels:
            label_entity = None
            for label in label_data:
                if label.get('id') == label_id:
                    label_entity = label
                    break

            if not label_entity:
                print(f"Лейбл {label_id} из доски {board_entity['title']} "
                      f"не найден в label.json")
                continue

            if label_entity['title'] in FORBIDDEN_TITLES:
                print(f"Стикер с названием '{label_entity['title']}' "
                      f"был пропущен.")
                continue

            # Conditional label
            if 'states' in label_entity:
                label_states = label_entity['states']['index']
                for state_id in label_states:
                    state = label_states[state_id]
                    label_instance = Label(
                        board_id=board_entity['planka_id'],
                        name=f"{label_entity['title']}: {state['name']}",
                        color=state['planka_color'],
                        created_at=timestamp_format(label_entity['timestamp']),
                        position=position_iterator
                    )
                    
                    created_label_data = persist(
                        label_instance, 
                        {   # unique keys
                            'name': label_instance.name,
                            'board_id': label_instance.board_id
                        }
                    )

                    if created_label_data is None:
                        print(f'Лейбл {label_entity["title"]} '
                              'является дублем и не будет создан!')
                        continue
                    else:
                        print(f'Лейбл {label_instance.name} создан на '
                              f'доске {board_entity['title']}.')
                        state['planka_id'] = created_label_data.id
                        position_iterator += 50
            # Simple label
            else:
                label_instance = Label(
                    board_id=board_entity['planka_id'],
                    name=label_entity['title'],
                    color='egg-yellow',
                    created_at=timestamp_format(label_entity['timestamp']),
                    position=position_iterator
                )

                created_label_data = persist(
                    label_instance, 
                    {   # unique keys
                        'name': label_instance.name,
                        'board_id': label_instance.board_id
                    }
                )

                if created_label_data is None:
                    print(f'Лейбл {label_entity["title"]} '
                          f'является дублем и не будет создан!')
                    continue
                else:
                    print(f'Лейбл {label_instance.name} создан на '
                          f'доске {board_entity['title']}.')
                    label_entity['planka_id'] = created_label_data.id
                    position_iterator += 50


save_json('label.json', label_data)
print('Готово. Импорт успешно завершен. '
      'Идентификаторы Planka добавлены в json. '
      'Для отмены импорта воспользуйтесь service.undo.undo_per_type()')
