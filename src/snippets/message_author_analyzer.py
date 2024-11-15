from src.services.data import load_json


def message_author_analyzer():
    tasks = load_json('task.json')
    users = load_json('user.json')

    unique_list = set()

    for task in tasks:
        chat = task.get('chat', {})
        messages = chat.get('messages', {})

        for timestamp, message in messages.items():
            if 'properties' not in message or 'displayName' not in message['properties']:
                from_id = message.get('from')
                if from_id:
                    unique_list.add(from_id)

    user_email_map = {user['id']: user['planka_email'] for user in users}

    for from_id in unique_list:
        email = user_email_map.get(from_id, "НЕ НАЙДЕН")
        print(f"{from_id} - {email}")


message_author_analyzer()
