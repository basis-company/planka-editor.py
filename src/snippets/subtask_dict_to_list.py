from src.services.data import load_json, save_json


def dict_to_list(data):
    """Рекурсивно преобразует словарь subtasks в массив словарей."""
    if isinstance(data, dict):
        if "subtaskList" in data:
            subtask_list = data["subtaskList"]
            if "subtasks" in subtask_list and isinstance(subtask_list["subtasks"], dict):
                subtask_list["subtasks"] = list(subtask_list["subtasks"].values())

        for key, value in data.items():
            dict_to_list(value)

    elif isinstance(data, list):
        for item in data:
            dict_to_list(item)
    return data


def main():
    data = load_json("task.json")
    transformed_data = dict_to_list(data)
    save_json("task.json", transformed_data)
    print('Done!')


if __name__ == "__main__":
    main()
