'''
Сниппет добавляет значение is_due_date, необходимое
для импорта работы статуса "done" карточек.
'''
from src.services.data import load_json, save_json


def process_task(task):
    if "planka_is_due_date_completed" in task:
        # Case 1: deadline from stickers
        deadline = (
            task.get("stickers", {})
                .get("00050d5a-64a9-49a6-8bec-f883d8909173", {})
                .get("current", {})
                .get("deadline")
        )
        if deadline is not None:
            task["planka_due_date"] = deadline
            print(f'[Case 1] В {task["id"]} добавлен ключ planka_due_date.')
        else:
            # Case 2: data.gtd.history.stage is done
            history = (
                task.get("data", {})
                .get("gtd", {})
                .get("history")
            )
            if history is not None:
                max_done_timestamp = max(
                    (int(ts) for ts, data in history.items() if data.get("stage") == "done"),
                    default=None
                )
                if max_done_timestamp is not None:
                    task["planka_due_date"] = max_done_timestamp
                else:
                    # Case 3: current task timestamp
                    task["planka_due_date"] = task.get("timestamp")

    # Recursion for subtasks
    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtasks:
        process_task(subtask)


def main():
    tasks = load_json("task.json")

    for task in tasks:
        process_task(task)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
