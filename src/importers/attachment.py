import re

from src.models.card import Card

from src.crud import database

from src.services.upload import persist_attachment


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


def identify_attachments(text, context, card_id=None):
    """Находит в тексте ссылки на файлы, создает вложения на их
    основе и заменяет ссылки в тексте на актуальные planka url."""
    # regex patterns
    # url_pattern = re.compile(r'https?://[^\s)]+')
    url_pattern = re.compile(r'https?://[^\s),"]+')
    file_pattern = re.compile(r"/root/#file:/user-data/([a-f0-9-]+)/(.+)")

    links = url_pattern.findall(text)
    if not links:
        return text

    # external yougile file links
    for link in links:
        if "yougile.com" in link:
            # print(f"[identify_attachments] YouGile URL found: {link}")
            attachment = persist_attachment(link, card_id, context)
            if attachment:
                new_url = (
                    f"https://planka.basis.services/"
                    f"attachments/{attachment['id']}/"
                    f"download/{attachment['name']}"
                )
                print(f"[identify_attachments] Attachment added: {new_url}")
                text = text.replace(link, new_url)

    # internal yougile file links
    file_matches = file_pattern.findall(text)
    for file_id, file_name in file_matches:
        new_file_url = (
            f"https://ru.yougile.com/user-data/"
            f"{file_id}/"
            f"{file_name}"
        )
        print(f"[identify_attachments] Attachment added: {new_file_url}")
        attachment = persist_attachment(new_file_url, card_id, context)
        if attachment:
            text = text.replace(f"/root/#file:/user-data/"
                                f"{file_id}/{file_name}", new_file_url)

    if card_id:
        update_card_description(card_id, text)

    return text
