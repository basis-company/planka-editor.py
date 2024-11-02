import json
import os

from constants import DATA_DIR


def load_json(file_name, data_dir=None):
    """
    Загружает данные из указанного JSON-файла.

    Args:
        file_name (str): Имя файла JSON.
        data_dir (str, optional): Директория с файлами JSON. 
                                  Если не указана, работает с src/data.

    Returns:
        data (list | dict): JSON, либо пустой список при ошибке.
    """
    if data_dir is None:
        data_dir = DATA_DIR
    file_path = os.path.join(data_dir, file_name)

    if not os.path.exists(file_path):
        print(f"[load_json] Файл {file_name} не найден в папке "
              f"{data_dir}. Он будет создан.")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({}, file)  # Создаём пустой JSON-объект
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[load_json] Ошибка: Файл {file_name} не найден в папке "
              f"{data_dir}!")
        return []


def save_json(file_name, data, data_dir=None):
    """
    Сохраняет данные в указанный JSON-файл.

    Args:
        file_name (str): Имя файла JSON.
        data (list | dict): Данные для сохранения.
        data_dir (str, optional): Директория для сохранения JSON.
                                  Если не указана, работает с src/data.
    """
    if data_dir is None:
        data_dir = DATA_DIR
    file_path = os.path.join(data_dir, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    # print(f"Данные успешно сохранены в {file_path}")
