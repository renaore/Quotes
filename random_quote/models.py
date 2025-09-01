from django.db import models

class Quote(models.Model):
    source = models.CharField()
    text = models.CharField()
    weight = models.IntegerField()
    shows = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)