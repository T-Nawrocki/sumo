from django.db import models

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class Banzuke(ValidateModelMixin, models.Model):
    """The rankings of competitor Rikishi in a Basho."""

    # META
    def __str__(self):
        return f"Banzuke for {self.basho}"

    class Meta:
        verbose_name_plural = "Banzuke"

    # RELATIONSHIPS
    basho = models.OneToOneField("basho.Basho", on_delete=models.CASCADE)
    competitors = models.ManyToManyField("rikishi.Rikishi", through='banzuke.BanzukeAppearance')
