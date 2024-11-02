"""
Сниппет находит коды цветов тегов в src/data/label.json и вычисляет
ближайший цвет из стандартных цветов plankanban. Результат складывается
в ключ planka_color в виде названия цвета, для дальнейшего импорта
досок с тегами.
"""

import json
import os

from constants import DATA_DIR


# Planka colors
color_dict = {
    'berry-red': '#e04556',
    'pumpkin-orange': '#f0982d',
    'lagoon-blue': '#109dc0',
    'pink-tulip': '#f97394',
    'light-mud': '#c7a57b',
    'orange-peel': '#fab623',
    'bright-moss': '#a5c261',
    'antique-blue': '#6c99bb',
    'dark-granite': '#8b8680',
    'lagune-blue': '#00b4b1',
    'sunny-grass': '#bfca02',
    'morning-sky': '#52bad5',
    'light-orange': '#ffc66d',
    'midnight-blue': '#004d73',
    'tank-green': '#8aa177',
    'gun-metal': '#355263',
    'wet-moss': '#4a8753',
    'red-burgundy': '#ad5f7d',
    'light-concrete': '#afb0a4',
    'apricot-red': '#fc736d',
    'desert-sand': '#edcb76',
    'navy-blue': '#166a8f',
    'egg-yellow': '#f7d036',
    'coral-green': '#2b6a6c',
    'light-cocoa': '#87564a',
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return None
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# Вычисляет Евклидово расстояние
def euclidean_distance(color1, color2):
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


# Находит ближайший цвет из planka
def find_closest_color(target_color):
    closest_color_name = None
    min_distance = float('inf')
    
    for name, color in color_dict.items():
        distance = euclidean_distance(target_color, color)
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
            
    return closest_color_name


# Ищет цвета тегов из YouGile/Trello и добавляет planka_color
def add_planka_color(data):
    if isinstance(data, dict):
        changes = []
        for key, value in data.items():
            if key == 'color':
                if not value or (isinstance(value, str) and not value.strip()):
                    closest_color_name = 'berry-red'  # Подставляем berry-red
                else:
                    closest_color_name = find_closest_color(value)
                
                changes.append(('planka_color', closest_color_name))
            else:
                add_planka_color(value)

        for key, val in changes:
            data[key] = val

    elif isinstance(data, list):
        for item in data:
            add_planka_color(item)


def process_json_file(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    add_planka_color(data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


file_name = 'label.json'
process_json_file(file_name)

print("Обработка завершена!")
