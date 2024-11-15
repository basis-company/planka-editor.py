from src.services.data import load_json, save_json


users = load_json("user.json")

# добавить пользователей
users_mapping = {
    "Имя Фамилия": ["displayName"]
}


base_id = "0000bdc7-0363-4d30-b5d3-5e0fc72f811f"
timestamp = int(1731408384 * 1000)
data_type = "User"

# словарь транслитераций
translit_dict = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    ' ': '.', 'ь': '', 'ъ': ''
}


def transliterate(name):
    """Преобразует русский текст в латиницу."""
    return ''.join(translit_dict.get(char, char) for char in name.lower())


def generate_email(full_name):
    name_parts = full_name.split()
    email_username = ".".join(transliterate(part) for part in name_parts)
    return f"{email_username}@basis.company"


for name in users_mapping.keys():
    new_user = {
        "id": base_id,
        "timestamp": timestamp,
        "dataType": data_type,
        "title": name,
        "location": "",
        "email": generate_email(name)
    }
    users.append(new_user)


save_json("user.json", users)
print("Новые пользователи успешно добавлены.")
