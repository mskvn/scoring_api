import redis


class Store:
    SOCKET_TIMEOUT = 5

    def __init__(self, host='localhost', port=6379):
        self._client = redis.Redis(host=host, port=port, socket_timeout=self.SOCKET_TIMEOUT)

    def get(self, name):
        return self._client.get(name)

    cache_get = get

    def cache_set(self, key, value, ttl):
        self._client.set(name=key, value=value, ex=ttl)
