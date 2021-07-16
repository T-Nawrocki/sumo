from django.db import models
from django.db.models.query_utils import Q
from django.db.models.constraints import UniqueConstraint

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class Heya(ValidateModelMixin, models.Model):
    """A heya (stable). Primarily acts as a collection of Rikishi."""

    # META
    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name_plural = "Heya"
        constraints = [
            UniqueConstraint(fields=['name'], condition=Q(is_active=True), name='unique_name_for_active_heya')
        ]

    # MODEL FIELDS
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # CLEANING
    def clean(self):
        self.name = self.name.lower()

    # PROPERTIES
    @property
    def full_name(self):
        return f"{self.name.capitalize()}-beya"
