"""
Итерация 1: Импортер для уровня проектов.
"""

from datetime import datetime
from src.models.project import Project
from src.models.project_manager import ProjectManager

from src.crud import persist
from src.services.data import load_json, save_json
from src.services.timestamp import timestamp_format


project_data = load_json('project.json')
if not project_data:
    print('Файл project.json не найден или пуст!')
    project_data = []

project_manager_data = load_json('project_manager.json')
if not project_manager_data:
    print('Файл project_manager.json не найден или пуст!')
    project_manager_data = []


# Projects
for project_entity in project_data:
    project_instance = Project(
        created_at=timestamp_format(project_entity['timestamp']),
        name=project_entity['title']
    )

    unique_keys = {'name': project_instance.name}
    created_project_data = persist(
        instance=project_instance,
        unique_keys=unique_keys
    )
    if created_project_data is None:
        print(f'Проект {project_entity["title"]} уже был создан ранее!')
        continue
    else:
        print(f'Проект {project_entity["title"]} создан.')
        project_entity['planka_id'] = created_project_data.id

    # Project managers
    for manager in project_manager_data:
        manager_instance = ProjectManager(
            user_id=manager['planka_id'],
            project_id=created_project_data.id
        )
        _unique_keys = {
            'project_id': manager_instance.project_id,
            'user_id': manager_instance.user_id 
        }
        created_project_manager = persist(manager_instance, _unique_keys)
        if created_project_manager is None:
            print(f'- Менеджер {manager["planka_email"]} уже фигурирует '
                  f'в проекте {project_entity["title"]}!')
        else:
            print(f'- Менеджер {manager["planka_email"]} добавлен в проект.')


# Update projects.json
save_json('project.json', project_data)
print('Проекты и менеджеры успешно импортированы в Planka. '
      'Данные сохранены в project.json')
