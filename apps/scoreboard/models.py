from django.db import models

class News(models.Model):
    text = models.TextField(max_length=4096, null=False, blank=False)
    created_at =  models.DateTimeField(auto_now_add=True)