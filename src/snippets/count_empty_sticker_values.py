from src.services.data import load_json


stickers_to_check = [
    "faeb509b-05d5-416b-8406-d3aa16fbd50a",
    "cbe605a0-57c0-4f20-a58b-a00597f38e00",
    "087f72ee-913a-4f35-8623-5cc603ac6e4d",
    "b69968e1-6794-47e4-8645-108924722136"
]


def count_empty_sticker_values():
    tasks = load_json('task.json')

    empty_counts = {sticker: 0 for sticker in stickers_to_check}

    for task in tasks:
        if 'stickers' in task:
            stickers = task['stickers']
            for sticker_uuid, state in stickers.items():
                if sticker_uuid in stickers_to_check and state == "":
                    empty_counts[sticker_uuid] += 1

    for sticker_uuid, count in empty_counts.items():
        print(f"Стикер {sticker_uuid} имеет {count} пустых значений.")


count_empty_sticker_values()
