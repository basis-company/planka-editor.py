import re
import urllib.parse
from src.services.data import load_json, save_json


def encode_file_name(encoded_url):
    """Декодирует Кириллические названия для файлов"""
    decoded_url = urllib.parse.unquote(urllib.parse.unquote(encoded_url))

    return decoded_url


def extract_file_name(url):
    """
    Извлекает название файла из ссылки, учитывая кодировку и удаляя лишние параметры.
    """
    url = encode_file_name(url)
    url_without_params = url.split('?')[0]
    file_name = urllib.parse.unquote(url_without_params).split('/')[-1]

    return file_name


def clean_html(text):
    return re.sub(r"</?[^>]+>", "", text)


def find_links(
    text: str,
    from_comment: bool = False,
    comment_date: int = None,
    tasks: list = None  # Передаем tasks для поиска полного ID
):
    """
    Находит в тексте ссылки и возвращает массив словарей со следующими полями:
    id: int,
    url_old: str,
    url_new: str,
    from_comment: bool,
    is_attachment: bool,
    is_card: bool,
    comment_date: int (if from_comment is True)
    """
    # regex patterns
    # url_pattern = r"https?://[^\s\"']+"
    # url_pattern = r"https?://[^\s\"']+(?=\s|$|[.,!?)]|\Z)"
    # url_pattern = r"https?://[^\s\"'>]+(?=\s|<\/?[^>]+>|$)"
    url_pattern = r"https?://[^\s\"'<>#]+(?:#[^\s\"'<>]*)?"
    internal_pattern = r"/root/#file:[^\s\"']+"
    attachment_pattern = r"yougile\.com/user-data"
    card_pattern = r"https://[^\s\"']+yougile\.com/team[^\s\"']+"

    urls = re.findall(url_pattern, text)
    internal_links = re.findall(internal_pattern, text)

    filtered_urls = [url for url in urls if re.search(attachment_pattern, url)]
    yougile_links = [url for url in urls if re.search(card_pattern, url)]

    all_links = set(filtered_urls + internal_links + yougile_links)

    result = []
    for link in all_links:
        is_attachment = bool(
            re.search(attachment_pattern, link) or
            re.search(internal_pattern, link)
        )
        is_card = bool(re.search(card_pattern, link))

        clean_link = clean_html(link)

        link_data = {
            "id": None,
            "url_old": clean_link,
            "url_new": "",
            "from_comment": from_comment,
            "is_attachment": is_attachment,
            "is_card": is_card
        }

        if is_attachment:
            file_name = extract_file_name(clean_link)
            link_data["file_name"] = file_name

        if is_card:
            card_id_match = re.search(
                r"yougile\.com/team/[a-f0-9\-]+/#chat:([a-f0-9]+)",
                link
            )
            if card_id_match:
                shortened_card_id = card_id_match.group(1)

                for task in tasks:
                    full_task_id = task['id']  # card_id
                    if full_task_id.endswith(shortened_card_id):
                        link_data["card_id"] = full_task_id
                        break

        if from_comment:
            link_data["comment_date"] = comment_date

        result.append(link_data)

    return result


def process_tasks(file_name):
    """
    Обрабатывает файл с карточками, добавляя каждой ключ planka_links.
    :param file_name: Название JSON-файла с карточками из src.data.
    """
    tasks = load_json(file_name)

    def process_task(task):
        """
        Рекурсивно обрабатывает задачу и ее подзадачи.
        :param task: Текущая задача для обработки.
        """
        planka_links = []

        # find in description
        description = task.get('description', '')
        if description:
            planka_links.extend(find_links(description, tasks=tasks))

        # find in comments
        planka_action = task.get('planka_action', [])
        for action in planka_action:
            comment_text = action.get('data', '')
            if comment_text:
                comment_links = find_links(
                    comment_text,
                    from_comment=True,
                    comment_date=action['created_at'],
                    tasks=tasks
                )
                planka_links.extend(comment_links)

        unique_links = {
            tuple(link.items()): link for link in planka_links
        }
        unique_links_list = list(unique_links.values())

        if unique_links_list:
            task['planka_links'] = unique_links_list

        subtasks = task.get('data', {}).get('subtaskList', {}).get('subtasks', [])
        for subtask in subtasks:
            process_task(subtask)

    for task in tasks:
        process_task(task)

    save_json(file_name, tasks)
    print('Done!\n')


if __name__ == "__main__":
    process_tasks('task.json')
