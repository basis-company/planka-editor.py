'''
Анализирует наличие ключа data.by и их значения на готовность к импорту
'''

from src.services.data import load_json


def analyze_data_by_field():
    entities = load_json('task.json')

    count_with_by = 0
    count_without_by = 0

    unique_by_values = set()

    for entity in entities:
        if 'data' in entity and 'by' in entity['data']:
            count_with_by += 1
            unique_by_values.add(entity['data']['by'])
        else:
            count_without_by += 1

    print(f"Количество сущностей с ключом 'data.by': {count_with_by}")
    print(f"Количество сущностей без ключа 'data.by': {count_without_by}")
    for value in unique_by_values:
        print(value)


analyze_data_by_field()
