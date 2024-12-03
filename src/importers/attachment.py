import re

from src.models.card import Card

from src.crud import database


def update_card_description(card_id: int, text: str) -> None:
    """Обновляет описание карточки в базе."""
    with database() as session:
        # card_instance = session.query(Card).get(card_id)
        card_instance = session.get(Card, card_id)
        if not card_instance:
            raise LookupError(f"[ERROR] Card with id {card_id} not found!")
        card_instance.description = text
        session.commit()

    print(f"[update_card_description] Card {card_id} "
          f"description was successfully updated.")


def detect_attachments(text):  # TODO: переделать после md-конвертации
    """Находит в тексте ссылки на файлы"""
    links = []

    # regex patterns
    links.extend(
        re.compile(r'https?://yougile\.com[^\s),"]*')
        .findall(text)
    )
    links.extend(
        re.compile(r"/root/#file:/user-data/([a-f0-9-]+)/(.+)")
        .findall(text)
    )

    if not links:
        return links

    # external yougile file links
    for link in links:
        if "yougile.com" in link:
            attachment = persist_attachment(link)
            if attachment:
                new_url = (
                    f"https://planka.basis.services/"
                    f"attachments/{attachment['id']}/"
                    f"download/{attachment['name']}"
                )
                print(f"[detect_attachments] Attachment added: {new_url}")
                text = text.replace(link, new_url)

    # internal yougile file links
    for file_id, file_name in file_matches:
        new_file_url = (
            f"https://ru.yougile.com/user-data/"
            f"{file_id}/"
            f"{file_name}"
        )
        print(f"[detect_attachments] Attachment added: {new_file_url}")
        attachment = persist_attachment(new_file_url)
        if attachment:
            text = text.replace(f"/root/#file:/user-data/"
                                f"{file_id}/{file_name}", new_file_url)

    return links
