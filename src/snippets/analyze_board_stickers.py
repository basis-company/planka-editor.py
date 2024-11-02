"""
Сниппет проверяет связи между досками и тегами в JSON-файлах,
находящихся в src/data. По завершению выводит кол-во оборванных связей.
Использовался для проверки связей перед импортом досок на проекты.
"""

import json
import os

from constants import DATA_DIR


def load_json(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_name} не найден в папке data.")
        return []


def analyze_board_stickers():
    boards = load_json('board.json')
    tags = load_json('label.json')

    valid_sticker_ids = {tag['id'] for tag in tags}
    invalid_sticker_count = 0

    for board in boards:
        board_title = board.get('title', 'Без названия')
        stickers = board.get('stickers', [])

        for sticker_id in stickers:
            if sticker_id in valid_sticker_ids:
                print(f"Доска '{board_title}' содержит валидный стикер "
                      f"{sticker_id}.")
            else:
                print(f"Доска '{board_title}' содержит НЕвалидный стикер "
                      f"{sticker_id}!")
                invalid_sticker_count += 1

    print(f"\nАнализ завершён. Количество невалидных стикеров: "
          f"{invalid_sticker_count}")

if __name__ == "__main__":
    analyze_board_stickers()
