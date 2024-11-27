from src.services.data import load_json, save_json


def main(tasks):
    label_positions = {}

    def process_task(task):
        if "planka_card_label" in task:
            for label in task["planka_card_label"]:
                board_id = label["board_id"]
                name = label["name"]

                if board_id not in label_positions:
                    label_positions[board_id] = {}

                if name not in label_positions[board_id]:
                    label_positions[board_id][name] = len(label_positions[board_id]) * 1000 + 1000

                label["board_position"] = label_positions[board_id][name]

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
