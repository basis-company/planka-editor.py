from src.services.data import load_json
from constants import TASK_FILE_NAME


def analyze_import(filename: str):
    tasks = load_json(filename)

    def process_task(task, recursive: bool = False):
        task_id = task.get("id")
        is_archived = task.get("planka_card_is_archived", True)
        planka_id = task.get("planka_id")

        if not planka_id and is_archived is True:
            if recursive:
                print(f"R {task_id}")
            else:
                print(f"  {task_id}")

        sub_tasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
        for sub_task in sub_tasks:
            process_task(sub_task, recursive=True)

    for task in tasks:
        process_task(task)


if __name__ == "__main__":
    analyze_import(TASK_FILE_NAME)
