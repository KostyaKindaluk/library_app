from django.db import models

class Genres(models.Model):
    title = models.CharField(max_length=30)


