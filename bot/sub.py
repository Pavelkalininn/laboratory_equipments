
class UserRequestStatus:
    """User request status and data by id."""
    storage = {}

    def __init__(self, telegram_id, status, data):
        self.storage[telegram_id] = (status, data)

    def remove(self, telegram_id):
        self.storage.pop(telegram_id)

    def exists(self, telegram_id):
        return bool(self.storage.get(telegram_id))
