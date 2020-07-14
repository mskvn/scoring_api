import os
import unittest

import docker
from docker.errors import NotFound


class TestSuite(unittest.TestCase):
    dockerfile = os.path.join(os.path.dirname(__file__), '../..')
    docker_client = client = docker.from_env()

    def setUp(self):
        self.remove_containers(['scoring_api', 'redis'])
        self.docker_client.containers.run(image='redis:alpine',
                                          name='redis',
                                          detach=True)

        self.docker_client.images.build(path='.', tag='scoring_api', dockerfile='dockerfiles/Dockerfile')
        self.docker_client.containers.run(image='scoring_api',
                                          ports={8080: 8080},
                                          name='scoring_api',
                                          command=' python ./api.py -a 0.0.0.0 --cache_host=redis',
                                          links={'redis': 'redis'},
                                          detach=True)

        print('debug')

    def tearDown(self):
        self.remove_containers(['scoring_api', 'redis'])

    def remove_containers(self, containers):
        for container_name in containers:
            try:
                container = self.docker_client.containers.get(container_name)
                container.stop()
                container.remove(force=True)
            except NotFound:
                print(f'Container {container_name} already removed')

    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()
