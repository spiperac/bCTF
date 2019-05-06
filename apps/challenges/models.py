import os
from django.db import models
from apps.accounts.models import Account


class Category(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=False, blank=False)
    author = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    points = models.IntegerField()
    visible = models.BooleanField(default=True)

    @property
    def sorted_by_solves_set(self):
        return self.solves.order_by('points')


class Hint(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)


class Flag(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)


class Attachment(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    data = models.FileField(upload_to='media/attachments/', max_length=500)

    def filename(self):
        return os.path.basename(self.data.name)


class Solves(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='solves', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='solves', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None):
        self.account.points += self.challenge.points
        self.account.save()
        super().save()

    def delete(self, *args, **kwargs):
        if self.account.points > self.challenge.points:
            self.account.points -= self.challenge.points
        else:
            self.account.points = 0
        self.account.save()
        super().delete(*args, **kwargs)


class FirstBlood(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BadSubmission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    flag = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
