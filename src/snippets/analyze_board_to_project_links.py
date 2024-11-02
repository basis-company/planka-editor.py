"""
Сниппет проверяет связи между досками и проектами в JSON-файлах,
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


def analyze_board_to_project_links():
    boards = load_json('board.json')
    projects = load_json('project.json')

    project_ids = {project['id'] for project in projects}
    not_found_count = 0

    for board in boards:
        board_location = board.get('location')
        board_location_name = board.get('location_PROJECT')
        board_title = board.get('title', 'Без названия')

        if board_location in project_ids:
            print(f"Доска '{board_title}' обнаружена "
                  f"в проекте {board_location_name}.")
        else:
            print(f"Доска '{board_title}' не обнаружена ни в одном из проектов. "
                  f"Ссылается на {board_location}.")
            not_found_count += 1

    print(f"\nАнализ завершён. Количество досок "
          f"без связи с проектом: {not_found_count}")


if __name__ == "__main__":
    analyze_board_to_project_links()
