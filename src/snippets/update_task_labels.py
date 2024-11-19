from src.services.data import load_json, save_json


def update_task_labels():
    tasks = load_json("task.json")
    labels = load_json("labels.json")

    for task in tasks:
        planka_labels = {"labels": [], "NOT_FOUND": {}}
        planka_users = {}
        stickers = task.get("stickers", {})

        # if "user" sticker found 
        if "00034c16-00b9-4ac7-ab24-fb60dc92ec5e" in stickers:
            for user in stickers["00034c16-00b9-4ac7-ab24-fb60dc92ec5e"]:
                planka_users[user] = ""
            stickers.pop("00034c16-00b9-4ac7-ab24-fb60dc92ec5e", None)

        for sticker_id, state_id in stickers.items():
            sticker = labels.get(sticker_id)

            if sticker:
                # simple sticker
                if state_id == "":
                    if "planka_id" in sticker:
                        planka_labels["labels"].append({
                            "name": sticker["title"],
                            "planka_id": sticker["planka_id"]
                        })
                    else:
                        planka_labels["NOT_FOUND"][sticker_id] = sticker["title"]
                # conditional stickers with one state
                elif isinstance(state_id, str):
                    state = sticker.get("states", {}).get("index", {}).get(state_id)
                    if state:
                        planka_labels["labels"].append({
                            "name": f'{sticker["title"]}: {state["name"]}',
                            "planka_id": state["planka_id"]
                        })
                    else:
                        planka_labels["NOT_FOUND"][state_id] = f'{sticker["title"]}: {state["name"]}' 
                # conditional stickers with multiple states
                elif isinstance(state_id, list):
                    for state_item in state_id:
                        state = sticker.get("states", {}).get("index", {}).get(state_item)
                        if state:
                            planka_labels["labels"].append({
                                "name": f'{sticker["title"]}: {state["name"]}',
                                "planka_id": state["planka_id"]
                            })
                        else:
                            planka_labels["NOT_FOUND"][state_item] = f'{sticker["title"]}: {state["name"]}'
            else:
                planka_labels["NOT_FOUND"][sticker_id] = ""

        if planka_labels["labels"] or planka_labels["NOT_FOUND"]:
            task["planka_labels"] = planka_labels

        if planka_users:
            task["planka_users"] = planka_users

    save_json("task.json", tasks)
    print('[update_task_labels] Done!')


update_task_labels()
