from src.services.data import load_json, save_json


def remove_key_from_task(task, key_to_remove):
    """Рекурсивно удаляет указанный ключ из всех карточек"""
    if key_to_remove in task:
        del task[key_to_remove]

    if task.get("data", {}).get("subtaskList", {}).get("subtasks"):
        for subcard in task["data"]["subtaskList"]["subtasks"]:
            remove_key_from_task(subcard, key_to_remove)


if __name__ == "__main__":
    filename = "task.json"
    tasks = load_json(filename)

    cards_count = 0
    subcards_count = 0

    for task in tasks:
        cards_count += 1
        if task.get("data", {}).get("subtaskList", {}).get("subtasks"):
            subcards_count += len(task["data"]["subtaskList"]["subtasks"])
        remove_key_from_task(
            task,
            key_to_remove="planka_links"
        )
    print(
        f"    {cards_count} cards\n"
        f"    {subcards_count} subcards\n"
        f"[remove_key_from_tasks] Done!\n"
    )

    save_json(filename, tasks)
