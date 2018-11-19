from django.db import models


class Configuration(models.Model):
    key = models.CharField(max_length=512, null=False, blank=False)
    value = models.CharField(max_length=2048, null=True, blank=True)

    def __str__(self):
        return self.key


class News(models.Model):
    text = models.TextField(max_length=4096, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
