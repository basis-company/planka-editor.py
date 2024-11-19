import re
from src.services.data import load_json, save_json
from src.services.markdown import html_to_markdown


def is_html(content):
    return bool(re.search(r'<.*?>', content))


def convert_and_store(task_data):
    for task in task_data:
        description = task.get("description")
        if description and is_html(description):
            task["planka_description"] = html_to_markdown(description)

        chat = task.get("chat", {})
        messages = chat.get("messages", {})
        for message_id, message in messages.items():
            if isinstance(message, dict):
                text = message.get("text")
                if text and isinstance(text, str) and is_html(text):
                    message["text"] = html_to_markdown(text)

    save_json("task.json", task_data)
    print('Конвертация в Markdown завершена!')


def main():
    task_data = load_json("task.json")
    convert_and_store(task_data)


main()
