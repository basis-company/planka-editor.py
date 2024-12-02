import time
import httpx
from typing import Optional
from io import BytesIO

from src.services.auth import get_access_token

from src.models.transaction import TransactionContext


def persist_attachment(
    file_url,
    card_id,
    context: Optional["TransactionContext"] = None
):
    api_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    # # retry parameters
    # retries = 5
    # delay = 0.3  # seconds

    # # availability checking
    # def is_card_available(card_id, headers):
    #     url = f"https://planka.basis.services/cards/{card_id}"
    #     with httpx.Client() as client:
    #         response = client.get(url, headers=headers)
    #         return response.status_code == 200

    # # retry logic
    # for attempt in range(retries):
    #     if is_card_available(card_id, headers):
    #         break
    #     else:
    #         print(f"[persist_attachment] Карточка {card_id} недоступна. "
    #               f"Попытка {attempt + 1} из {retries}. Ожидание {delay} сек.")
    #         if attempt < retries - 1:
    #             time.sleep(delay)
    #         else:
    #             print(f"[persist_attachment] Карточка {card_id} не была найдена "
    #                   f"после {retries} попыток.")
    #             return None

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
                    response.headers.get(
                        'Content-Type',
                        'application/octet-stream'
                    )
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
            # print(f'    [ATTACHMENT DATA]: {attachment_data}')
            attachment_id = attachment_data['item']['id']
            print(f"[persist_attachment] Вложение "
                  f"{attachment_id} создано: {file_name}")

            if context:
                context.log_entity("Attachment", attachment_id)

            return {'id': attachment_id, 'name': file_name}

    except Exception as e:
        print(f"[persist_attachment] Ошибка при создании вложения: {e}")
        return None


def remove_attachment(
    file_id,
    context: Optional["TransactionContext"] = None
):
    api_token = get_access_token()
    headers = {'Authorization': f'Bearer {api_token}'}

    url = f'https://planka.basis.services/api/attachments/{file_id}'

    try:
        with httpx.Client() as client:
            response = client.delete(url, headers=headers, timeout=10.0)
            response.raise_for_status()

            if response.status_code == 200:
                print(f"    Attachment: {file_id} was successfully removed.")
                if context:
                    context.log_entity("Attachment", file_id)
                return True
            else:
                print(f"[Warning] Attachment: {file_id} Not removed for some "
                      f"reason and will be kept in. Response status: "
                      f"{response.status_code}")
                return False

    except Exception as e:
        print(f"[remove_attachment] Error deleting attachment: {e}")
        return False
