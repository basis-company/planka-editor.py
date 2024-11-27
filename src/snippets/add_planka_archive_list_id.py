from src.services.data import load_json, save_json


def process_tasks(task, archive_mapping):
    if task.get("planka_card_is_archived") is True:
        board_id = str(task.get("planka_board_id"))
        if board_id in archive_mapping:
            task["planka_archive_list_id"] = archive_mapping[board_id]
            # print(f'    Добавлен ключ для {task['title']}')

    # recursion
    subtask_list = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtask_list:
        process_tasks(subtask, archive_mapping)


def main():
    tasks = load_json("task.json")
    archive_mapping = load_json("archive_list_mapping.json")

    for task in tasks:
        process_tasks(task, archive_mapping)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
