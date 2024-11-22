from src.services.data import load_json, save_json


def remove_sticker_key(task, key_to_remove):
    if 'stickers' in task:
        task['stickers'].pop(key_to_remove, None)

    if 'data' in task and 'subtaskList' in task['data']:
        for subtask in task['data']['subtaskList']['subtasks']:
            remove_sticker_key(subtask, key_to_remove)


def process_tasks(file_name, key_to_remove):
    tasks = load_json(file_name)

    for task in tasks:
        remove_sticker_key(task, key_to_remove)

    save_json(file_name, tasks)
    print("[main] Done!")


process_tasks('task.json', 'bdfd1e08-8496-48cf-a420-b26310bd3a2c')
