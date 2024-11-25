from src.services.upload import upload_attachment


def persist_attachment(card):
    file_url = 'code_me'  # TODO: Attachment detection logic based on description
    card_id = card['id']
    return upload_attachment(file_url, card_id)
