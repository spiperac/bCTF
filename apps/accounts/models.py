from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def rank(self):
        pass