from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class Torikumi(ValidateModelMixin, models.Model):

    # META
    def __str__(self):
        return f"Torikumi for {self.basho} day {self.day}"

    class Meta:
        verbose_name_plural = "Torikumi"

    # MODEL FIELDS
    basho = models.ForeignKey("basho.basho", on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
