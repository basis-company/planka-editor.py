from src.services.data import load_json


def display_name_analyzer():
    tasks = load_json('task.json')
    usernames = {}

    for task in tasks:
        if 'chat' in task and 'messages' in task['chat']:
            messages = task['chat']['messages']

            for timestamp, message in messages.items():
                if 'properties' in message and 'displayName' in message['properties'] and 'from' in message:
                    username = message['properties']['displayName']
                    user_from = message['from']

                    if username not in usernames:
                        usernames[username] = set()
                    usernames[username].add(user_from)

    for username, from_values in usernames.items():
        from_list = ', '.join(from_values)
        print(f"{username} - {from_list}")


display_name_analyzer()
