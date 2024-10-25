import os
import json
from datetime import datetime
from src.models.project import Project
from src.models.project_manager import ProjectManager
from src.crud import persist


project_json_path = 'src/data/project.json'
if not os.path.exists(project_json_path):
    print(f'Файл {project_json_path} не найден!')
else:
    with open(project_json_path, 'r') as project_file:
        project_data = json.load(project_file)

project_manager_json_path = 'src/data/project_manager.json'
if not os.path.exists(project_manager_json_path):
        print(f'Файл {project_manager_json_path} не найден!')
else:
    with open(project_manager_json_path, 'r') as project_manager_file:
        managers = json.load(project_manager_file)


# Projects
for project_entity in project_data:
    project_instance = Project(
        created_at=datetime.fromtimestamp(project_entity['timestamp'] / 1000),
        name=project_entity['title']
    )

    unique_keys = {'name': project_instance.name}
    created_project_data = persist(project_instance, unique_keys)
    if created_project_data is None:
        print(f'Проект {project_entity["title"]} уже был создан ранее!')
        continue
    else:
        print(f'Проект {project_entity["title"]} создан.')
        project_entity['planka_id'] = created_project_data.id

    # Project managers
    for manager in managers:
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
            print(f'- Менеджер {manager["planka_email"]} уже присутствует в проекте {project_entity["title"]}!')
        else:
            print(f'- Менеджер {manager["planka_email"]} добавлен в проект.')


# Update projects.json
with open(project_json_path, 'w') as project_file:
    json.dump(project_data, project_file, indent=4)

print(f'Проекты и менеджеры успешно импортированы в Planka. '
      f'Данные сохранены в {project_json_path}')
