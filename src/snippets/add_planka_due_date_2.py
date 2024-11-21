from src.services.data import load_json, save_json


def process_task(task):
    stickers_key = "00050d5a-64a9-49a6-8bec-f883d8909173"
    stickers = task.get("stickers", {})

    if stickers_key in stickers:
        deadline = stickers[stickers_key].get("current", {}).get("deadline")
        if deadline is not None:
            task.setdefault("planka_due_date", deadline)

        del stickers[stickers_key]

        if not stickers:
            del task["stickers"]

        if "planka_is_due_date_completed" not in task:
            task["planka_is_due_date_completed"] = False

    # Recursion for subtasks
    subtask_list = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtask_list:
        process_task(subtask)


def main():
    tasks = load_json("task.json")
    for task in tasks:
        process_task(task)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
