import os
from django.db import models
from apps.accounts.models import Account


class Category(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, null=False, blank=False)
    description = models.TextField(max_length=8192, null=False, blank=False)
    points = models.IntegerField()
    visible = models.BooleanField(default=True)

    @property
    def sorted_by_solves_set(self):
        return self.solves_set.order_by('points')


class Hint(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)


class Flag(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)


class Attachment(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    data = models.FileField(upload_to='media/attachments/')

    def filename(self):
        return os.path.basename(self.data.name)


class Solves(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class FirstBlood(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
