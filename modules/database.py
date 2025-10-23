from redis import Redis

class Database:
  _connection: Redis

  def __init__(self, redis_url: str) -> None:
    self._connection = Redis.from_url(redis_url)

  def save(self, entries: dict[str, str]) -> None:
    HOUR = 60 * 60
    for key, value in entries.items():
      self._connection.set(key, value, ex=HOUR * 24)

  def close(self) -> None:
    self._connection.close()

