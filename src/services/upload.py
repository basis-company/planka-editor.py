from io import BytesIO
from src.services.auth import get_access_token

import httpx


def upload_attachment(file_url, card_id):
    api_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {api_token}',
    }

    if '/' in file_url:
        *_, file_name = file_url.split('/')
    else:
        file_name = 'Untitled'
        # raise ValueError('В url файла не найден разделитель /')

    url = f'https://planka.basis.services/api/cards/{card_id}/attachments'
    result = ''

    try:
        with httpx.Client() as client:
            response = client.get(file_url)
            response.raise_for_status()

            file_content = BytesIO(response.content)
            files = {
                "file": (
                    file_name,
                    file_content,
                    response['Content-Type']
                )
            }

            result = client.post(
                url,
                headers=headers,
                files=files,
                timeout=10.0
            )

            result.raise_for_status()

    except Exception as e:
        print(e)

    return result
