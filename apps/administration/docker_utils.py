import docker
import logging


logger = logging.getLogger(__name__)


class DockerTool(object):

    def __init__(self):
        self.host = None
        self.key = None

        self.client = None
        self.api_client = None
        self.connect()

    def connect(self):
        try:
            self.client = docker.from_env()
            self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
            self.client.create_host_config(
                publish_all_ports=True,
            )

        except Exception as exception:
            logger.error("Unable to connect to docker host: {0}".format(exception))

    def list_containers(self):
        return self.client.containers.list(all=True)

    def list_images(self):
        return self.client.images.list()

    def get_container(self, container_id):
        return self.client.containers.get(container_id)

    def get_image(self, image_id):
        return self.client.images.get(image_id)

    def remove_image(self, image_id):
        self.api_client.remove_image(image_id)

    def create_image(self, path, image_name):
        return self.api_client.build(
            path=path,
            rm=True,
            quiet=True,
            tag=image_name)

    def create_container(self, image_id):
        return self.client.containers.create(image_id, publish_all_ports=True)

    def container_action(self, container_id, action):
            container = self.get_container(container_id)

            if action == "restart":
                container.restart()
            elif action == "stop":
                container.stop()
            elif action == "pause":
                if container.status == "paused":
                    container.unpause()
                else:
                    container.pause()
            elif action == "start":
                container.start()
            elif action == "remove":
                container.remove()
            else:
                return False
            return True

    def execute(self, container_id, cmd):
        container = self.get_container(container_id)
        output = container.exec_run(cmd)
        return output
