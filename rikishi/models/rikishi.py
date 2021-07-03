from django.db import models

from common.mixins.validate_model_mixin import ValidateModelMixin


class RikishiManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class Rikishi(ValidateModelMixin, models.Model):
    """
        A rikishi (sumo wrestler).

        Rikishi are one of the core objects for the application.
        Rikishi belong to a Heya and come from a Shusshin, which both act primarily
        as collections of Rikishi.
    """

    # MANAGER
    objects = RikishiManager()

    # MODEL FIELDS
    name_first = models.CharField(max_length=255)
    name_second = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    birth_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    height = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

    # RELATIONSHIPS
    heya = models.ForeignKey(
        'rikishi.heya',
        on_delete=models.CASCADE
    )
    shusshin = models.ForeignKey(
        'rikishi.shusshin',
        on_delete=models.CASCADE
    )
