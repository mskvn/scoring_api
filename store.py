import logging
import time
from functools import wraps

import redis
from redis.exceptions import TimeoutError, ConnectionError

from exceptions import StoreGetException


def retry(tries=3, delay=0.5):
    def deco_retry(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            local_tries, local_delay = tries, delay
            while local_tries > 0:
                try:
                    return f(*args, **kwargs)
                except (TimeoutError, ConnectionError) as e:
                    msg = '{}, Retrying in {} seconds...'.format(e, local_delay)
                    logging.info(msg)
                    time.sleep(local_delay)
                    local_tries -= 1
            return f(*args, **kwargs)

        return wrapper

    return deco_retry


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
        return value

    def cache_get(self, name):
        try:
            return self.get_with_retry(name)
        except Exception as e:
            logging.error(str(e))
            return None

    def cache_set(self, key, value, ttl=None):
        try:
            self.set_with_retry(key, value, ttl)
        except Exception as e:
            logging.error(str(e))

    @retry(tries=3)
    def set_with_retry(self, key, value, ttl=None):
        self._client.set(name=key, value=value, ex=ttl)

    @retry(tries=3)
    def get_with_retry(self, name):
        return self._client.get(name)
