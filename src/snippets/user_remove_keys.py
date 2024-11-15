from src.services.data import load_json, save_json


users = load_json("user.json")

for user in users:
    user.pop("language", None)
    user.pop("skin", None)

save_json("user.json", users)

print("Ключи 'language' и 'skin' успешно удалены.")
