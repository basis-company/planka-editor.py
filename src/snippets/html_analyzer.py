import re
from src.services.data import load_json


def extract_html_tags(text):
    """Находит все HTML-теги в переданном тексте."""
    if not isinstance(text, str):
        return []
    return re.findall(r"<(/?\w+)[^>]*>", text)


def main():
    task_data = load_json("task.json")

    all_tags = set()

    for task in task_data:
        # check description
        description = task.get("description")
        if description:
            all_tags.update(extract_html_tags(description))

        # check chat.messages
        chat = task.get("chat", {})
        messages = chat.get("messages", [])
        for message in messages:
            if isinstance(message, dict):
                for key, value in message.items():
                    if isinstance(value, str):
                        all_tags.update(extract_html_tags(value))

    # print unique html tags
    print("Найденные HTML-теги:")
    for tag in sorted(all_tags):
        print(f"<{tag}>")


main()
