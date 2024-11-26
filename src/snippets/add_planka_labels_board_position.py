from src.services.data import load_json, save_json


def main(tasks):  # TODO: Проверить результат
    label_positions = {}

    def process_task(task):
        if "planka_card_label" in task:
            for label in task["planka_card_label"]:
                board_id = label["board_id"]
                name = label["name"]
                key = (board_id, name)

                if key not in label_positions:
                    # board label position logic
                    label_positions[key] = len(label_positions) * 1000 + 1000

                label["board_position"] = label_positions[key]

        if "data" in task and "subtaskList" in task["data"]:
            subtasks = task["data"]["subtaskList"].get("subtasks", [])
            for subtask in subtasks:
                process_task(subtask)

    for task in tasks:
        process_task(task)

    print('[main] Done!')


tasks = load_json("task.json")
main(tasks)
save_json("task.json", tasks)
