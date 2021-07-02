from django.db import models


class Heya (models.Model):
    """A heya (stable). Primarily acts as a collection of Rikishi."""

    name = models.CharField(max_length=255)
