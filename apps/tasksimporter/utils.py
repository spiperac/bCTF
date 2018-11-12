import yaml
import os
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from apps.challenges.models import Challenge, Category, Flag, Hint, Attachment


class Task:
    def __init__(self, name, category, description, flag, points, attachments=[]):
        self.name = name
        self.category = category
        self.description = description
        self.flag = flag
        self.points = points
        self.attachments = attachments

    def create(self):
        # Category
        if Category.objects.filter(name=self.category).count() == 0:
            Category.objects.create(name=self.category)

        # Challenge
        category_obj = Category.objects.get(name=self.category)
        challenge_obj = Challenge.objects.create(
            name=self.name,
            category=category_obj,
            description=self.description,
            points=self.points
        )

        # Flag
        Flag.objects.create(
            challenge=challenge_obj,
            text=self.flag
        )

        # Attachments
        if self.attachments is not None:
            for attachment in self.attachments:
                fs = FileSystemStorage()
                file_obj = open(attachment, 'rb')
                filename = fs.save("{0}".format(file_obj.name), file_obj)
                uploaded_file_url = fs.url(filename)

                new_attachment = Attachment.objects.create(
                    challenge=challenge_obj,
                )
                new_attachment.data.save(file_obj.name.split("/")[-1], file_obj)


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


def parse_task_yaml(task_dir):
    with open("{0}/{1}".format(task_dir, "task.yml")) as data_file:
        task = yaml.load(data_file)
    if validate_task_file(task):
        attachments = []
        if 'attachments' in task:
            if task['attachments']:
                for attachment in task['attachments']:
                    attachment_file = "{0}/files/{1}".format(task_dir, attachment)
                    if os.path.isfile(attachment_file):
                        attachments.append(attachment_file)

        new_task = Task(
            name=task['name'],
            category=task['category'],
            description=task['description'],
            flag=task['flag'],
            points=task['points'],
            attachments=attachments
        )
        return new_task
    else:
        return False


def feed_tasks(base_path):
    task_list = locate_tasks(base_path)

    tasks = []
    for task_dir_name in task_list:
        print("Trying to add {}".format(task_dir_name))
        task_full_path = "{0}/{1}".format(base_path, task_dir_name)
        if os.path.isfile("{0}/task.yml".format(task_full_path)):
            new_task = parse_task_yaml(task_full_path)
            if new_task:
                tasks.append(new_task)

    return tasks
