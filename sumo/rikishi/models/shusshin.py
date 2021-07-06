from sumo.common.utils import choices_as_dict
from django.core.exceptions import ValidationError
from django.db import models

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin
from sumo.geography import prefectures
from sumo.geography import countries


class Shusshin (ValidateModelMixin, models.Model):
    """A shusshin (place of origin). Primarily acts as a collection of Rikishi."""

    def __str__(self):
        if self.prefecture:
            return prefectures.full_display_name(self.prefecture)
        else:
            return choices_as_dict(countries)[self.country]


    # MODEL FIELDS
    town = models.CharField(max_length=255)
    prefecture = models.CharField(
        max_length=255,
        choices=prefectures.PREFECTURES,
        blank=True
    )
    country = models.CharField(
        max_length=255,
        choices=countries.COUNTRIES,
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
