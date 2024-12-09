from src.services.data import load_json
'''
Возможные расширения файлов из вложений:
avi	    js	    PNG
csv	    lua	    pptx
doc	    mov	    svg
docx	mp4	    txt
exe	    msg	    vsd
gif	    ovpn	xls
html	pdf	    XLS
jpeg	PDF	    xlsx
jpg	    pdm	    xml
JPG	    png	    zip
'''


def analyze_file_names(task, file_names):
    """
    Рекурсивно извлекает все значения file_name из 
    planka_links и добавляет их в список без дублей.
    """
    if 'planka_links' in task:
        for link in task['planka_links']:
            if 'file_name' in link:
                file_names.add(link['file_name'])

    if 'data' in task and 'subtaskList' in task['data']:
        for subtask in task['data']['subtaskList'].get('subtasks', []):
            analyze_file_names(subtask, file_names)


if __name__ == "__main__":
    tasks = load_json("task.json")
    file_names = set()
    for task in tasks:
        analyze_file_names(task, file_names)

    for file_name in file_names:
        print(file_name)
