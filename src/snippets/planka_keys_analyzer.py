from src.services.data import load_json


TASK_COUNTER = 0


def process_task(task, is_subtask=False):
    global TASK_COUNTER
    TASK_COUNTER += 1

    task_type = "Да" if is_subtask else "Нет"

    list_id = task.get("planka_list_id")
    board_id = task.get("planka_board_id")

    if list_id is None and board_id is None:
        print(f'    {task["id"]} - не найдены ключи "planka_list_id" и "planka_board_id". Subtask: {task_type}')
    elif list_id is None:
        print(f'    {task["id"]} - не найден ключ "planka_list_id". Subtask: {task_type}')
    elif board_id is None:
        print(f'    {task["id"]} - не найден ключ "planka_board_id". Subtask: {task_type}')

    # Recursion for subtasks
    subtask_list = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtask_list:
        process_task(subtask, is_subtask=True)


def main():
    tasks = load_json("task.json")
    for task in tasks:
        process_task(task)

    print(f"Операция завершена. Всего было обработано {TASK_COUNTER} карточек.")


if __name__ == "__main__":
    main()
