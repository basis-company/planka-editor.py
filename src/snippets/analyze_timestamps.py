from src.services.data import load_json


def find_oldest_and_newest_tasks(tasks):
    oldest_task = None
    newest_task = None

    def process_task(task):
        nonlocal oldest_task, newest_task

        if oldest_task is None or task["timestamp"] < oldest_task["timestamp"]:
            oldest_task = task
        if newest_task is None or task["timestamp"] > newest_task["timestamp"]:
            newest_task = task

        subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
        for subtask in subtasks:
            process_task(subtask)

    for task in tasks:
        process_task(task)

    return oldest_task, newest_task


if __name__ == "__main__":
    tasks = load_json("task.json")

    oldest_task, newest_task = find_oldest_and_newest_tasks(tasks)

    print(f"Oldest task {oldest_task['id']}: {oldest_task['timestamp']}")
    print(f"Newest task {newest_task['id']}: {newest_task['timestamp']}")
    print(f"Diff: {newest_task['timestamp'] - oldest_task['timestamp']}")
