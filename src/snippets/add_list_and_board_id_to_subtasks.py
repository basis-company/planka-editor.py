from src.services.data import load_json, save_json


def propagate_keys_to_subtasks(task, inherited_keys):
    for key, value in inherited_keys.items():
        task.setdefault(key, value)

    subtask_list = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])

    # Recursion for subtasks
    for subtask in subtask_list:
        propagate_keys_to_subtasks(subtask, inherited_keys)


def main():
    tasks = load_json("task.json")

    for task in tasks:
        inherited_keys = {
            "planka_list_id": task.get("planka_list_id"),
            "planka_board_id": task.get("planka_board_id"),
        }

        propagate_keys_to_subtasks(task, inherited_keys)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
