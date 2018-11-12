import json
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


def parse_tasks_yaml(base_path, yaml_data):
    if 'tasks' in yaml_data:
        tasks = []
        for task in yaml_data['tasks']:
            attachments = []
            if 'attachments' in task:
                if task['attachments']:
                    for attachment in task['attachments']:
                        attachments.append("{0}/{1}/files/{2}".format(base_path, task['dir_name'], attachment['file']))

            new_task = Task(
                name=task['name'],
                category=task['category'],
                description=task['description'],
                flag=task['flag'],
                points=task['points'],
                attachments=attachments
            )
            tasks.append(new_task)
        return tasks
