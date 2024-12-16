from src.services.data import load_json, save_json


def main(tasks):
    count_removed = 0

    def remove_deprecated_membership(task_list):
        nonlocal count_removed
        for task in task_list:
            if (
                task.get("timestamp", 0) < 1690837200000
                and len(task.get("planka_card_membership", [])) == 1
                and task["planka_card_membership"][0].get("planka_user_id") == 1357309142464726393
            ):
                del task["planka_card_membership"]
                count_removed += 1

            subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
            if subtasks:
                remove_deprecated_membership(subtasks)

    remove_deprecated_membership(tasks)
    return count_removed


if __name__ == "__main__":
    tasks = load_json("task.json")
    removed_count = main(tasks)
    save_json("task.json", tasks)
    print(f"Number of tasks where 'planka_card_membership' "
          f"was removed: {removed_count}")
