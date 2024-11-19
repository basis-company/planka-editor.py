'''
Сниппет генерирует участников в task.json
на основании различных связей с юзерами.
'''
from src.services.data import load_json, save_json


def main():
    task_data = load_json("task.json")
    user_data = load_json("user.json")

    user_lookup = {user["id"]: user for user in user_data}

    for task in task_data:
        # stickers
        stickers = task.get("stickers", {})
        if "00034c16-00b9-4ac7-ab24-fb60dc92ec5e" in stickers:
            sticker_values = stickers["00034c16-00b9-4ac7-ab24-fb60dc92ec5e"]

            if isinstance(sticker_values, str):
                sticker_values = [sticker_values]

            task["planka_card_membership"] = []

            for value in sticker_values:
                user = user_lookup.get(value)
                if user:
                    task["planka_card_membership"].append({
                        "planka_user_id": user.get("planka_id"),
                        "planka_created_at": user.get("timestamp"),
                        "planka_email": user.get("planka_email")
                    })

            stickers.pop("00034c16-00b9-4ac7-ab24-fb60dc92ec5e")

        if not stickers:
            task.pop("stickers", None)

        # data.by
        data_by = task.get("data", {}).get("by")
        if data_by:
            if "planka_card_membership" not in task:
                task["planka_card_membership"] = []

            if isinstance(data_by, str):
                data_by = [data_by]

            existing_user_ids = {member["planka_user_id"] for member in task["planka_card_membership"]}

            for user_id in data_by:
                user = user_lookup.get(user_id)
                if user and user.get("planka_id") not in existing_user_ids:
                    task["planka_card_membership"].append({
                        "planka_user_id": user.get("planka_id"),
                        "planka_created_at": user.get("timestamp"),
                        "planka_email": user.get("planka_email")
                    })
                    existing_user_ids.add(user.get("planka_id"))

        # data.assignedBy
        assigned_by = task.get("data", {}).get("assignedBy", {})
        if assigned_by:
            if "planka_card_membership" not in task:
                task["planka_card_membership"] = []

            existing_user_ids = {member["planka_user_id"] for member in task["planka_card_membership"]}

            for user_id in assigned_by.keys():
                user = user_lookup.get(user_id)
                if user and user.get("planka_id") not in existing_user_ids:
                    task["planka_card_membership"].append({
                        "planka_user_id": user.get("planka_id"),
                        "planka_created_at": user.get("timestamp"),
                        "planka_email": user.get("planka_email")
                    })
                    existing_user_ids.add(user.get("planka_id"))

    save_json("task.json", task_data)
    print('Done!')


main()
