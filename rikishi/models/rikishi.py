from datetime import date

from django.core.exceptions import ValidationError
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

    # CLEANING
    def _validate_first_name_is_unique(self):
        matching_rikishi_exists = Rikishi.objects.exclude(id=self.id).filter(
            is_active=True,
            name_first=self.name_first,
        ).exists()
        if matching_rikishi_exists:
            raise ValidationError('An active Rikishi already exists with that first name.')

    def _validate_age(self):
        if self.age < 15:
            raise ValidationError('Rikishi cannot be under 15.')

    def clean(self):
        self.name_first = self.name_first.lower()
        self.name_second = self.name_second.lower()

        self._validate_first_name_is_unique()
        self._validate_age()

    # PROPERTIES
    @property
    def age(self):
        today = date.today()
        # int(True) == 1, so if True, this will reduce age by 1
        not_yet_had_birthday_this_year = ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return today.year - self.date_of_birth.year - not_yet_had_birthday_this_year

