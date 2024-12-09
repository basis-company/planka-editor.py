from src.services.data import load_json, save_json
from src.services.markdown import html_to_markdown


def add_planka_description(task):
    """
    Рекурсивно обрабатывает task и его вложенные subtasks.
    Преобразует поле description в Markdown и сохраняет 
    результат в planka_description.
    """

    if 'description' in task:
        task['planka_description'] = html_to_markdown(task['description'])
    else:
        task['planka_description'] = None

    # recursion for subcards
    subtasks = task.get('data', {}).get('subtaskList', {}).get('subtasks', [])
    for subtask in subtasks:
        add_planka_description(subtask)


def main():
    tasks = load_json("task.json")
    for task in tasks:
        add_planka_description(task)
    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main()
