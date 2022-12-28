from const import (
    REDIS_HOST,
    STATUS,
    STATUS_TYPE,
)
from redis import (
    Redis,
)


class MessageInfo:
    """User request status and data by id."""
    storage = Redis(host=REDIS_HOST)

    def delete(self, user_id: int) -> None:
        user_id = str(user_id)
        headers = self.storage.hkeys(str(user_id))
        if headers:
            self.storage.hdel(user_id, *list(headers))

    def exists(self, user_id: int):
        return bool(self.storage.hgetall(name=str(user_id)))

    def set_status(self, user_id: int, status: str) -> None:
        self.storage.hset(str(user_id), STATUS, status)

    def set_status_type(self, user_id: int, status_type: str) -> None:
        self.storage.hset(str(user_id), STATUS_TYPE, status_type)

    def set_item(self, user_id: int, key: str, value: str) -> None:
        self.storage.hset(str(user_id), key, value)

    def set_mapping(self, user_id: int, mapping: dict) -> None:
        self.storage.hset(str(user_id), mapping=mapping)

    def get_status(self, user_id: int) -> str:
        status = self.storage.hget(str(user_id), STATUS)
        return status.decode() if status else None

    def get_status_type(self, user_id: int) -> str:
        status_type = self.storage.hget(str(user_id), STATUS_TYPE)
        return status_type.decode() if status_type else None

    def get_data_value(self, user_id: int, key: str) -> str:
        value = self.storage.hget(str(user_id), key)
        return value.decode() if value else None

    def get_user_info(self, user_id: int) -> dict:
        return {
            key.decode(): value.decode()
            for key, value in self.storage.hgetall(
                str(user_id)
            ).items()
        }

    def get_data(self, user_id: int) -> dict:
        result = self.get_user_info(user_id)
        if result:
            if STATUS in result:
                result.pop('status')
            if STATUS_TYPE in result:
                result.pop('status_type')
        return result

    def remove_data_value(self, user_id: int, keys: list) -> None:
        self.storage.hdel(str(user_id), *list(keys))
