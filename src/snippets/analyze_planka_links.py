import csv
from src.services.data import load_json


def analyze_planka_links(task, links_set):
    if 'planka_links' in task:
        for link in task['planka_links']:
            if 'url_old' in link and link['url_old']:
                if link['url_old'] != "//":
                    links_set.add(link['url_old'])

    if task.get('data', {}).get('subtaskList', {}).get('subtasks'):
        for subtask in task['data']['subtaskList']['subtasks']:
            analyze_planka_links(subtask, links_set)


def save_links_to_csv(links_set, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        # changed delimiter to semicolon
        writer = csv.writer(file, delimiter=';')
        for link in sorted(links_set):
            writer.writerow([link])


def extract_planka_links_with_conditions(task, result):
    """
    Рекурсивно обходит task и ищет url_old в planka_links,
    где is_attachment и from_comment равны true.
    """
    planka_links = task.get("planka_links", [])
    for link in planka_links:
        if link.get("is_attachment") is True and link.get("from_comment") is True:
            result.append(link.get("url_old"))

    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtasks:
        extract_planka_links_with_conditions(subtask, result)


def main():
    tasks = load_json("task.json")
    result = []

    for task in tasks:
        extract_planka_links_with_conditions(task, result)

    for url in result:
        print(url)


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     tasks = load_json('task.json')

#     links_set = set()

#     for task in tasks:
#         analyze_planka_links(task, links_set)

#     links_file_path = 'src/data/links.csv'
#     if os.path.exists(links_file_path):
#         os.remove(links_file_path)
#     save_links_to_csv(links_set, links_file_path)

#     print('Done! Links have been saved to links.csv.\n')
