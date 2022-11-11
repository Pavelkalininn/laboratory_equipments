from const import (
    REDIS_HOST,
)
from redis import (
    Redis,
)


class MessageInfo:
    """User request status and data by id."""
    storage = Redis(host=REDIS_HOST)

    def get(self, user_id: int):
        user_information = self.storage.hgetall(name=str(user_id)).items()
        if user_information:
            result = {
                key.decode(): value.decode()
                for key, value in user_information
            }
            status = ''
            status_type = ''
            if result:
                if 'status' in result:
                    status = result.pop('status')
                if 'status_type' in result:
                    status_type = result.pop('status_type')
            return (
                status,
                status_type,
                result or {})
        return None

    def set(self, user_id: int, value: tuple) -> None:
        self.delete(user_id)
        user_id = str(user_id)
        status, status_type, data = value
        if status:
            self.storage.hset(name=user_id, key='status', value=status)
        if status_type:
            self.storage.hset(
                name=user_id,
                key='status_type',
                value=status_type
            )
        if data:
            self.storage.hset(name=user_id, mapping=data)

    def delete(self, user_id: int) -> None:
        user_id = str(user_id)
        headers = self.storage.hkeys(user_id)
        if headers:
            self.storage.hdel(user_id, *list(headers))

    def exists(self, user_id: int):
        return bool(self.storage.hgetall(name=str(user_id)))
