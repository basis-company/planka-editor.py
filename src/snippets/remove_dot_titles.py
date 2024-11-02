"""
Сниппет удаляет системный мусор из src/data/label.json,
в частности названия тегов, которые начинаются с точки.
"""

import json
import os

from constants import DATA_DIR


def remove_dot_titles(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    filtered_data = [tag for tag in data if not tag['title'].startswith('.')]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    print("Объекты с title, начинающимися с точки, были удалены.")


if __name__ == "__main__":
    json_file_path = os.path.join(DATA_DIR, 'label.json')
    remove_dot_titles(json_file_path)
