# from uuid import uuid4
from datetime import datetime, timezone


class TransactionContext:
    def __init__(self):
        # self.transaction_id = str(uuid4())
        self.timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        self.created_entities = []

    def log_entity(self, entity_type, entity_id):
        self.created_entities.append({"type": entity_type, "id": entity_id})

    def get_transaction_data(self):
        return {
            # "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "entities": self.created_entities
        }
