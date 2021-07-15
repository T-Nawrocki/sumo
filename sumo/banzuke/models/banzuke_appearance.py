from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class BanzukeAppearance(ValidateModelMixin, models.Model):
    """
    Through-model mapping the many-to-many relationship between Rikishi and Banzuke.
    Contains rank information for the Rikishi's rank on this banzuke.
    Ranks are represented as integers for easy comparison.
    """

    class Meta:
        constraints = [models.UniqueConstraint(fields=['banzuke', 'rikishi'], name='unique_banzuke_appearance')]

    banzuke = models.ForeignKey("banzuke.banzuke", on_delete=models.CASCADE)
    rikishi = models.ForeignKey("rikishi.rikishi", on_delete=models.CASCADE)

    division = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    makuuchi_rank = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    numeric_rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
