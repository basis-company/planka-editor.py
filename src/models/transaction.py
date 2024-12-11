from datetime import datetime, timezone

from src.services.data import load_json, save_json

from constants import LOG_FILE_NAME


class TransactionContext:
    def __init__(self):
        self.timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        self.created_entities = []

    def write(self, entity_type, entity_id):
        self.created_entities.append({"type": entity_type, "id": entity_id})

    def rollback(self):
        self.created_entities = []

    def commit(self):
        uploaded_data = load_json(LOG_FILE_NAME) or {}
        if self.created_entities:
            uploaded_data[str(self.timestamp)] = self.created_entities
            save_json(LOG_FILE_NAME, uploaded_data)
