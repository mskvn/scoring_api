import os
import time
import unittest

import docker
import requests
from docker.errors import NotFound

from store import Store
from tests.integration.docker_utils import remove_containers


class TestSuite(unittest.TestCase):
    method_url = 'http://127.0.0.1:8080/method/'
    health_url = 'http://127.0.0.1:8080/_health/'

    dockerfile = os.path.join(os.path.dirname(__file__), '../..')
    docker_client = docker.from_env()

    @classmethod
    def setUpClass(cls):
        remove_containers(['scoring_api', 'redis'])
        cls.docker_client.containers.run(image='redis:alpine',
                                         name='redis',
                                         ports={6379: 6379},
                                         detach=True)

        cls.docker_client.images.build(path='.', tag='scoring_api', dockerfile='dockerfiles/Dockerfile')
        cls.docker_client.containers.run(image='scoring_api',
                                         ports={8080: 8080},
                                         name='scoring_api',
                                         command=' python ./api.py -a 0.0.0.0 --cache_host=redis',
                                         links={'redis': 'redis'},
                                         detach=True)
        cls.wait_app_ready()

    @classmethod
    def wait_app_ready(cls):
        timeout = 30
        max_time = time.time() + timeout
        while time.time() < max_time:
            try:
                response = requests.get(url=cls.health_url)
                if response.status_code == 200:
                    return
            except requests.exceptions.ConnectionError:
                print('App not ready yet...Try again')
                time.sleep(0.5)

        raise Exception(f"App does not ready within {timeout} sec")

    @classmethod
    def tearDownClass(cls):
        remove_containers(['scoring_api', 'redis'])

    def test_ok_score_request(self):
        request_body = {
            "account": "horns&hoofs",
            "login": "h&f",
            "method": "online_score",
            "arguments": {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru"
            },
            "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"
        }
        response = requests.post(self.method_url, json=request_body)
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body['code'], 200)
        score = response_body['response']['score']
        self.assertEqual(score, 3)

    def test_ok_score_request_using_cache(self):
        request_body = {
            "account": "horns&hoofs",
            "login": "h&f",
            "method": "online_score",
            "arguments": {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru"
            },
            "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"
        }
        response = requests.post(self.method_url, json=request_body)
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body['code'], 200)
        score = response_body['response']['score']
        self.assertEqual(score, 3.0)

        response = requests.post(self.method_url, json=request_body)
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body['code'], 200)
        score = response_body['response']['score']
        self.assertEqual(score, 3.0)

    def test_ok_interests_request_using_cache(self):
        client_ids = [1, 2, 3]
        request_body = {
            "account": "horns&hoofs",
            "login": "h&f",
            "method": "clients_interests",
            "arguments": {
                "client_ids": client_ids,
                "date": "04.07.2020"
            },
            "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"
        }
        store = Store()
        for id in client_ids:
            store.cache_set(f'i:{id}', f'{id}-interests')
        response = requests.post(self.method_url, json=request_body)
        self.assertEqual(response.status_code, 200)

    def test_invalid_interests_request_without_cache(self):
        client_ids = [1, 2, 3]
        request_body = {
            "account": "horns&hoofs",
            "login": "h&f",
            "method": "clients_interests",
            "arguments": {
                "client_ids": client_ids,
                "date": "04.07.2020"
            },
            "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"
        }
        response = requests.post(self.method_url, json=request_body)
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
