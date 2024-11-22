from src.services.data import load_json


def collect_missing_stickers(task, valid_labels, missing_stickers):
    stickers = task.get("stickers", {})

    for sticker_id in stickers.keys():
        if sticker_id not in valid_labels:
            missing_stickers.add(sticker_id)

    subtasks = task.get("data", {}).get("subtaskList", {}).get("subtasks", [])
    for subtask in subtasks:
        collect_missing_stickers(subtask, valid_labels, missing_stickers)


def main():
    tasks = load_json("task.json")
    labels = load_json("label.json")

    valid_labels = {label["id"] for label in labels}

    missing_stickers = set()

    for task in tasks:
        collect_missing_stickers(task, valid_labels, missing_stickers)

    print("Уникальные отсутствующие стикеры:")
    for sticker in sorted(missing_stickers):
        print(sticker)


if __name__ == "__main__":
    main()
