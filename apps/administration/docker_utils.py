import docker
import logging


logger = logging.getLogger(__name__)


class DockerTool(object):

    def __init__(self):
        self.host = None
        self.key = None

        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = docker.from_env()
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

    def create_container(self, image_id):
        return self.client.containers.create(image_id)

    def execute(self, container_id, cmd):
        container = self.get_container(container_id)
        output = container.exec_run(cmd)
        return output
