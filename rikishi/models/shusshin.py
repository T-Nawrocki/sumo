from django.db import models

from geography.countries import COUNTRIES
from geography.prefectures import PREFECTURES


class Shusshin (models.Model):
    """A shusshin (place of origin). Primarily acts as a collection of Rikishi."""

    town = models.CharField(max_length=255)
    prefecture = models.CharField(
        max_length=255,
        choices=PREFECTURES,
        blank=True
    )
    country = models.CharField(
        max_length=255,
        choices=COUNTRIES,
        default='JP'
    )
