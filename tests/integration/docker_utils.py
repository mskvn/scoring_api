import docker
from docker.errors import NotFound


def remove_containers(containers):
    docker_client = docker.from_env()
    for container_name in containers:
        try:
            container = docker_client.containers.get(container_name)
            container.stop()
            container.remove(force=True)
        except NotFound:
            print(f'Container {container_name} already removed')
