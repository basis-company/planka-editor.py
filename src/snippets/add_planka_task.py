from src.services.data import load_json, save_json


def process_checklists(task):
    checklists = task.get("data", {}).get("checklists", [])
    if not checklists:
        return

    planka_task = []

    for checklist in checklists:
        checklist_title = checklist.get("title", "")
        for item in checklist.get("items", []):
            planka_task.append({
                "id": item["id"],
                "isCompleted": item["isCompleted"],
                "name": f"{checklist_title} — {item['title']}"
            })

    task["planka_task"] = planka_task

    subtask_list = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtask_list:
        process_checklists(subtask)


def main():
    tasks = load_json("task.json")

    for task in tasks:
        process_checklists(task)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
