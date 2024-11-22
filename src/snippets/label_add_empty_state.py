from src.services.data import load_json, save_json


def add_empty_state(file_name):
    labels = load_json(file_name)

    for label in labels:
        if "states" not in label:
            label["states"] = {"index": {}}

        if "index" not in label["states"]:
            label["states"]["index"] = {}

        # new state
        label["states"]["index"]["blank"] = {
            "id": "",
            "name": label.get("title", ""),
            "color": "#AFB0A4",
            "planka_color": "light-concrete"
        }

    save_json(file_name, labels)
    print('[add_empty_state] Done!')


def fix_state_names(file_name):
    labels = load_json(file_name)

    for label in labels:
        if "states" in label:
            states = label['states']['index']
            for state in states.values():
                name = state['name']
                state['name'] = f"{label['title']}: {name}"

    save_json(file_name, labels)
    print('[fix_state_names] Done!')


fix_state_names("label.json")
add_empty_state("label.json")
