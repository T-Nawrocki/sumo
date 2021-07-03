from django.core.exceptions import ValidationError
from django.db import models

from common.mixins.validate_model_mixin import ValidateModelMixin
from geography.countries import COUNTRIES
from geography.prefectures import PREFECTURES


class Shusshin (ValidateModelMixin, models.Model):
    """A shusshin (place of origin). Primarily acts as a collection of Rikishi."""

    # MODEL FIELDS
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

    # CLEANING
    def _validate_prefecture(self):
        if self.country != 'JP' and self.prefecture:
            raise ValidationError('Foreign Shusshin cannot have a prefecture.')
        if self.country == 'JP' and not self.prefecture:
            raise ValidationError('Shusshin in Japan must specify a prefecture.')

    def clean(self):
        self._validate_prefecture()
