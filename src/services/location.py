from src.services.data import load_json


def get_location_planka_id(file_name, location_id):
    """
    Метод возвращает planka_id родительской сущности.

    Args:
        file_name (str): Имя файла JSON, содержащего родительские сущности (например, 'project.json').
        location_id (int): Идентификатор родительской сущности для поиска.

    Returns:
        int: Значение `planka_id` найденной сущности.

    Raises:
        ValueError: Если `planka_id` не найден или отсутствует сущность с данным ID.
    """
    parent_data = load_json(file_name) 

    for entity in parent_data:
        if entity.get('id') == location_id:
            planka_id = entity.get('planka_id')
            if planka_id is not None:
                return planka_id
            else:
                raise ValueError(f"[get_location_planka_id] ОШИБКА: Сущность "
                                 f"с id {location_id} не содержит planka_id!")

    raise ValueError(f"[get_location_planka_id] ОШИБКА: Сущность с "
                     f"id {location_id} не найдена в данных!")
