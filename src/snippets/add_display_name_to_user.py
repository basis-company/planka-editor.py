from src.services.data import load_json, save_json


users = load_json("user.json")

for user in users:
    if 'display_name' not in user:
        user['display_name'] = []

save_json("user.json", users)
print('Done!\n')
