from src.services.data import load_json, save_json


def remove_planka_id(data):
    if isinstance(data, dict):
        data.pop("planka_id", None)

        for key in data:
            remove_planka_id(data[key])
    elif isinstance(data, list):
        for item in data:
            remove_planka_id(item)


def main():
    data = load_json("label.json")
    remove_planka_id(data)
    save_json("label.json", data)
    print("Все ключи 'planka_id' успешно удалены из label.json.")


if __name__ == "__main__":
    main()
