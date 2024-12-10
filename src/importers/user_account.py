"""
Итерация 5: Импортируем бывших сотрудников,
для сохранения связей и комментариев.
"""
from src.models.user_account import UserAccount

from src.crud import persist
from src.services.data import load_json, save_json
from src.services.timestamp import timestamp_format


user_data = load_json('user.json')

# User
for user_entity in user_data:
    # создаем юзеров, которые еще не имеют planka_id
    if 'planka_id' not in user_entity:
        user_instance = UserAccount(
            email=user_entity['email'],
            is_admin=False,
            name=user_entity['title'],
            organization="Базис ИТ",
            subscribe_to_own_cards=False,
            created_at=timestamp_format(user_entity['timestamp']),
            is_sso=True
        )

        created_user_data = persist(
            instance=user_instance, 
            unique_keys={
                'email': user_instance.email,
                'name': user_instance.name
            }
        )

        if created_user_data is None:
            print(f'Пользователь {user_entity["email"]} '
                  'является дублем и не будет создан!')
            continue
        else:
            print(f"Пользователь {user_instance.email} создан.")
            user_entity['planka_id'] = created_user_data.id
            user_entity['planka_email'] = created_user_data.email


save_json('user.json', user_data)
print('Импорт успешно завершен. '
      'Идентификаторы Planka добавлены в json. '
      'Для отмены воспользуйтесь service.undo.undo_per_type()')
