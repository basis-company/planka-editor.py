from src.services.data import load_json, save_json


def add_title_prefix(tasks, is_recursive=False):
    for task in tasks:
        subtasks = (
            task.get("data", {})
            .get("subtaskList", {})
            .get("subtasks", None)
        )

        if subtasks is not None:
            task['title'] = "★ " + task.get('title', '')
            add_title_prefix(subtasks, is_recursive=True)

        if is_recursive:
            task['title'] = "☆ " + task.get('title', '')


def main():
    tasks = load_json("task.json")
    add_title_prefix(tasks)
    save_json("task.json", tasks)
    print("[main] Done!\n")


if __name__ == "__main__":
    main()
