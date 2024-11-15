from src.services.data import load_json, save_json


def user_remove_users(file_name, target_timestamp):
    data = load_json(file_name)
    print(f"Загружено {len(data)} сущностей.")  # Отладка: сколько сущностей в файле

    matching_entities = [entity for entity in data if entity.get('timestamp') == target_timestamp]
    print(f"Найдено {len(matching_entities)} сущностей с timestamp = {target_timestamp}.")

    filtered_data = [entity for entity in data if entity.get('timestamp') != target_timestamp]
    print(f"Осталось {len(filtered_data)} сущностей после фильтрации.")  # Отладка: сколько осталось

    save_json(file_name, filtered_data)
    print("Данные успешно сохранены.")


user_remove_users('user.json', 1731408384000)
