import logging

import redis

from exceptions import StoreGetException


class Store:
    SOCKET_TIMEOUT = 5

    def __init__(self, host='localhost', port=6379):
        pool = redis.ConnectionPool(host=host,
                                    port=port,
                                    decode_responses=True,
                                    socket_timeout=self.SOCKET_TIMEOUT)
        self._client = redis.Redis(connection_pool=pool)

    def get(self, name):
        value = self.cache_get(name)
        if not value:
            raise StoreGetException(f"Can not get value from store by key {name}")

    def cache_get(self, name):
        try:
            return self._client.get(name)
        except Exception as e:
            logging.error(str(e))
            return None

    def cache_set(self, key, value, ttl=None):
        try:
            self._client.set(name=key, value=value, ex=ttl)
        except Exception as e:
            logging.error(str(e))
