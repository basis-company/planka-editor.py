from src.services.data import load_json, save_json


def remove_gtd(task):
    if "gtd" in task.get("data", {}):
        del task["data"]["gtd"]
        # print(f'[remove_gtd] В {task["id"]} удален ключ gtd.')

    # Recursion for subtasks
    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtasks:
        remove_gtd(subtask)


def main():
    tasks = load_json("task.json")

    for task in tasks:
        remove_gtd(task)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
