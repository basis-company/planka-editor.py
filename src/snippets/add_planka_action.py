from src.services.data import load_json, save_json

users = load_json("user.json")
tasks = load_json("task.json")


def get_user_planka_id(user_id, display_name=None):
    if display_name:
        for user in users:
            if display_name in user.get("display_name", []):
                return user["planka_id"]

    if user_id:
        for user in users:
            if user["id"] == user_id:
                return user["planka_id"]

    print(f"    Пользователь не найден: {user_id} / {display_name}")
    return None


def process_task(task):
    if "chat" in task and "messages" in task["chat"]:
        messages = task["chat"]["messages"]
        planka_actions = []

        for *_, message in messages.items():
            if (
                "text" in message
                and message["text"]
                and message["text"] != "."
                and "from" in message
            ):
                user_id = message["from"]
                display_name = None

                if user_id == "0000bdc7-0363-4d30-b5d3-5e0fc72f811f":
                    display_name = message.get("properties", {}).get("display_name")

                planka_id = get_user_planka_id(user_id, display_name)

                if planka_id:
                    planka_actions.append({
                        "user_id": planka_id,
                        "data": message["text"],
                        "created_at": message["timestamp"]
                    })

        if planka_actions:
            task["planka_action"] = planka_actions

    if "data" in task and "subtaskList" in task["data"]:
        for subtask in task["data"]["subtaskList"].get("subtasks", []):
            process_task(subtask)


def main(task):
    for task in tasks:
        process_task(task)

    save_json("task.json", tasks)
    print('[main] Done!')


if __name__ == "__main__":
    main(tasks)
