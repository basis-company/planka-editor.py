import json
from datetime import datetime
from src.models.project import Project
from src.models.project_manager import ProjectManager
from src.crud import persist


project_json_path = 'src/data/project.json'
project_manager_json_path = 'src/data/project_manager.json'

with open(project_json_path, 'r') as project_file:
    project_data = json.load(project_file)

with open(project_manager_json_path, 'r') as project_manager_file:
    managers = json.load(project_manager_file)

uploaded_json_path = project_json_path.replace('.json', '_uploaded.json')
uploaded_data = []

for project_entity in project_data:
    project_instance = Project(
        created_at=datetime.fromtimestamp(project_entity['timestamp'] / 1000),
        name=project_entity['title']
    )

    created_project_data = persist(project_instance)
    print(f'Проект {project_entity['title']} создан.')
    project_entity['planka_id'] = created_project_data.id
    uploaded_data.append(project_entity)

    for manager in managers:
        manager_instance = ProjectManager(
            user_id=manager['planka_id'],
            project_id=created_project_data.id
        )
        persist(manager_instance)
        print(f'- Менеджер {manager['planka_email']} добавлен в проект.')

with open(uploaded_json_path, 'w') as uploaded_file:
    json.dump(uploaded_data, uploaded_file, indent=4)

print(f'Проекты и менеджеры успешно импортированы. '
      f'Данные сохранены в {uploaded_json_path}')
