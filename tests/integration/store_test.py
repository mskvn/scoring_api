import time
import unittest

import docker

from store import Store
from tests.integration.docker_utils import remove_containers


class StoreTest(unittest.TestCase):
    docker_client = docker.from_env()
    redis_port = 6380

    @classmethod
    def setUpClass(cls):
        remove_containers(['redis-store'])
        cls.docker_client.containers.run(image='redis:alpine',
                                         name='redis-store',
                                         ports={6379: cls.redis_port},
                                         detach=True)

    @classmethod
    def tearDownClass(cls):
        remove_containers(['scoring_api', 'redis'])

    def test_set_and_get(self):
        store = Store(port=self.redis_port)
        key = 'test'
        value = 'value'
        store.set_with_retry(key, value)
        actual = store.get(key)
        self.assertEqual(actual, value)

    def test_cache_set_and_get(self):
        store = Store(port=self.redis_port)
        key = 'test'
        value = 'value'
        store.cache_set(key, value)
        actual = store.get(key)
        self.assertEqual(actual, value)

    def test_set_and_cache_get(self):
        store = Store(port=self.redis_port)
        key = 'test'
        value = 'value'
        store.set_with_retry(key, value)
        actual = store.cache_get(key)
        self.assertEqual(actual, value)

    def test_get_not_exists_value(self):
        store = Store(port=self.redis_port)
        key = 'not_exists_key'
        with self.assertRaises(Exception) as exp:
            store.get(key)
        self.assertTrue(f'Can not get value from store by key {key}' in str(exp.exception))

    def test_cache_get_not_exists_value(self):
        store = Store(port=self.redis_port)
        key = 'not_exists_key'
        self.assertIsNone(store.cache_get(key))

    def test_set_with_ttl(self):
        store = Store(port=self.redis_port)
        key = 'test'
        value = 'value'
        ttl = 10
        store.set_with_retry(key, value, ttl)
        self.assertEqual(store.cache_get(key), value)
        time.sleep(ttl)
        self.assertIsNone(store.cache_get(key))


if __name__ == '__main__':
    unittest.main()
