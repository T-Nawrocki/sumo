from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


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

    # META
    def __str__(self):
        return self.shikona_display

    objects = RikishiManager()

    # BASIC MODEL FIELDS
    shikona_first = models.CharField(max_length=255, help_text="The rikishi's ring name.")
    shikona_second = models.CharField(max_length=255, help_text="The rikishi's ring name second name.")
    is_active = models.BooleanField(default=True)

    birth_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    height = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

    # HISTORY FIELDS
    shikona_history = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    heya_id_history = ArrayField(models.IntegerField(), default=list, blank=True)

    # RELATIONSHIPS
    heya = models.ForeignKey('rikishi.heya', on_delete=models.CASCADE)
    shusshin = models.ForeignKey('rikishi.shusshin', on_delete=models.CASCADE)

    # CLEANING, VALIDATION AND SAVING
    def _validate_first_name_is_unique(self):
        matching_rikishi_exists = Rikishi.objects.exclude(id=self.id).filter(
            is_active=True,
            shikona_first=self.shikona_first,
        ).exists()
        if matching_rikishi_exists:
            raise ValidationError('An active Rikishi already exists with that first name.')

    def _validate_age(self):
        if self.age < 15:
            raise ValidationError('Rikishi cannot be under 15.')

    def clean(self):
        self.shikona_first = self.shikona_first.lower()
        self.shikona_second = self.shikona_second.lower()

        if self.is_active:
            self._validate_first_name_is_unique()
        self._validate_age()

    def _update_shikona_history(self, old_data):
        has_new_name = not old_data.exists() or self.shikona_full != old_data.first().shikona_full
        if has_new_name and (not len(self.shikona_history) or self.shikona_history[-1] != self.shikona_full):
            self.shikona_history.append(self.shikona_full)

    def _update_heya_id_history(self, old_data):
        has_new_heya = not old_data.exists() or self.heya_id != old_data.first().heya_id
        if has_new_heya and (not len(self.heya_id_history) or self.heya_id_history[-1] != self.heya_id):
            self.heya_id_history.append(self.heya_id)

    def save(self, *args, **kwargs):
        self.full_clean()

        old_data = Rikishi.objects.filter(id=self.id)
        self._update_shikona_history(old_data)
        self._update_heya_id_history(old_data)

        super(Rikishi, self).save(*args, **kwargs)

    # PROPERTIES
    @property
    def age(self):
        today = date.today()
        # int(True) == 1, so if True, this will reduce age by 1
        not_yet_had_birthday_this_year = ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return today.year - self.date_of_birth.year - not_yet_had_birthday_this_year

    @property
    def shikona_full(self):
        return f"{self.shikona_first} {self.shikona_second}"

    @property
    def shikona_display(self):
        return self.shikona_full.title()
