from io import BytesIO
from src.services.auth import get_access_token

import httpx


def persist_attachment(file_url, card_id):
    api_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {api_token}',
    }

    # filename
    if '/' in file_url:
        *_, file_name = file_url.split('/')
    else:
        file_name = 'Untitled'

    url = f'https://planka.basis.services/api/cards/{card_id}/attachments'

    try:
        with httpx.Client() as client:
            response = client.get(file_url)
            response.raise_for_status()

            file_content = BytesIO(response.content)
            files = {
                "file": (
                    file_name,
                    file_content,
                    response.headers.get('Content-Type', 'application/octet-stream')
                )
            }

            result = client.post(
                url,
                headers=headers,
                files=files,
                timeout=10.0
            )

            result.raise_for_status()
            attachment_data = result.json()
            attachment_id = attachment_data['id']
            print(f"[persist_attachment] Вложение "
                  f"{attachment_id} создано: {file_name}")

            return {'attachment_id': attachment_id, 'filename': file_name}

    except Exception as e:
        print(f"[persist_attachment] Ошибка при создании вложения: {e}")
        return None
