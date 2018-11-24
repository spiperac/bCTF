import json
import zipfile
import os
import io
import shutil
from django.core.files.storage import FileSystemStorage
from apps.challenges.models import Attachment, Category, Challenge, Flag
from apps.administration.docker_utils import DockerTool


class Task:
    def __init__(self, name, category, description, flag, points, attachments=[], docker_path=False):
        self.name = name
        self.category = category
        self.description = description
        self.flag = flag
        self.points = points
        self.attachments = attachments
        self.docker_path = docker_path
        self.log = []

    def create_docker_image(self, path):
        dt = DockerTool()
        image_name = "".join(self.name.split()).lower()
        build = dt.create_image(path, "{0}/{1}".format(self.category, image_name))

        if build:
            self.log.append('Docker image created: {0}'.format(self.name))
        else:
            self.log.append('Error: Image creation failed for: {0}'.format(self.name))

    def create(self):
        self.log.append("Importing challenge: {0}".format(self.name))
        # Category
        if Category.objects.filter(name=self.category).count() == 0:
            Category.objects.create(name=self.category)
            self.log.append("Category {0} created.".format(self.category))

        # Challenge
        category_obj = Category.objects.get(name=self.category)
        challenge_obj = Challenge.objects.create(
            name=self.name,
            category=category_obj,
            description=self.description,
            points=self.points
        )
        self.log.append('Challenge added.')

        # Flag
        Flag.objects.create(
            challenge=challenge_obj,
            text=self.flag
        )
        self.log.append('Flag {0} added.'.format(self.flag))

        # Attachments
        if self.attachments is not None:
            for attachment in self.attachments:
                fs = FileSystemStorage()
                file_obj = open(attachment, 'rb')
                filename = fs.save("{0}".format(file_obj.name), file_obj)
                fs.url(filename)

                new_attachment = Attachment.objects.create(
                    challenge=challenge_obj,
                )
                new_file_name = file_obj.name.split("/")[-1]
                new_attachment.data.save(new_file_name, file_obj)
                self.log.append('Attachment {0} added.'.format(new_file_name))

        if self.docker_path:
            print(self.docker_path)
            self.create_docker_image(self.docker_path)

        self.log.append("Success!")


def locate_tasks(base_path):
    tasks_list = next(os.walk(base_path))[1]
    for folder in tasks_list:
        if folder.startswith("."):
            tasks_list.remove(folder)

    return tasks_list


def validate_task_file(task_data):
    schema = [
        'name',
        'category',
        'description',
        'flag',
        'points',
        'attachments'
    ]
    valid = True
    for item in schema:
        if item not in task_data:
            valid = False

    return valid


def parse_task_json(task_dir):
    with open("{0}/{1}".format(task_dir, "task.json")) as data_file:
        task = json.load(data_file)
    if validate_task_file(task):
        attachments = []
        docker_path = False

        if 'attachments' in task:
            if task['attachments'] is True:
                files_path = "{0}/files/".format(task_dir)
                attachments = [''.join((files_path, f)) for f in os.listdir(files_path) if os.path.isfile(''.join((files_path, f)))]

        if 'docker' in task:
            print('docker found!')
            if task['docker'] is True:
                docker_path = "{0}/docker/".format(task_dir)

        new_task = Task(
            name=task['name'],
            # author=task['author'],
            category=task['category'],
            description=task['description'],
            flag=task['flag'],
            points=task['points'],
            attachments=attachments,
            docker_path=docker_path
        )
        return new_task
    else:
        return False


def feed_tasks(base_path):
    task_list = locate_tasks(base_path)
    print(task_list)

    tasks = []
    for task_dir_name in task_list:
        print("Trying to add {}".format(task_dir_name))
        task_full_path = "{0}/{1}".format(base_path, task_dir_name)
        task_file = "{0}/task.json".format(task_full_path)
        print(task_file)
        if os.path.isfile(task_file):
            print("Adding new task")
            new_task = parse_task_json(task_full_path)
            if new_task:
                tasks.append(new_task)

    return tasks


def clean_base_path(base_path):
    shutil.rmtree(base_path, ignore_errors=True)


def export_as_zip():
    challenges = Challenge.objects.prefetch_related('flag_set').all()

    zip_file = io.BytesIO()
    archive  = zipfile.ZipFile(zip_file, "a")

    for challenge in challenges:
        task_json = {
            "name": challenge.name,
            "category": challenge.name,
            "description": challenge.description,
            "flag": "test",
            "points": challenge.points,
            "attachments": "true" if challenge.attachment_set.all() else "false"
        }

        archive.writestr("tasks/{0}/task.json".format(challenge.name), json.dumps(task_json))

        if challenge.attachment_set.count() > 0:
            for attachment in challenge.attachment_set.all():
                f = attachment.data.open(mode="rb")
                archive.writestr("{0}/files/{1}".format(challenge.name, str(os.path.basename(attachment.data.name))), f.read())
                f.close()

    for file in archive.filelist:
        file.create_system = 0

    archive.close()

    return zip_file
