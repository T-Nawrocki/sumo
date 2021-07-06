from django.core.exceptions import ValidationError
from django.db import models

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class Heya (ValidateModelMixin, models.Model):
    """A heya (stable). Primarily acts as a collection of Rikishi."""

    # MODEL FIELDS
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # CLEANING
    def _validate_name_is_unique(self):
        matching_heya_exists = Heya.objects.exclude(id=self.id).filter(
            is_active=True,
            name=self.name,
        ).exists()
        if matching_heya_exists:
            raise ValidationError('An active Heya already exists with that name.')

    def clean(self):
        self.name = self.name.lower()
        if self.is_active:
            self._validate_name_is_unique()

    # PROPERTIES
    @property
    def full_name(self):
        return f"{self.name.capitalize()}-beya"
