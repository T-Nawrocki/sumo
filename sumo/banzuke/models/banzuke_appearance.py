from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class BanzukeAppearance(ValidateModelMixin, models.Model):
    """
    Through-model mapping the many-to-many relationship between Rikishi and Banzuke.
    Contains rank information for the Rikishi's rank on this banzuke.
    Ranks are represented as integers for easy comparison.
    """

    # CONSTANTS
    # yapf: disable
    DIVISION_CHOICES = (
        (1, 'Makuuchi'),
        (2, 'Jūryō'),
        (3, 'Makushita'),
        (4, 'Sandanme'),
        (5, 'Jonidan'),
        (6, 'Jonokuchi')
    )

    DIVISION_ABBREVIATIONS = {
        1: '',
        2: 'J',
        3: 'Ms',
        4: 'Sd',
        5: 'Jd',
        6: 'Jk'
    }

    MAKUUCHI_RANK_CHOICES = (
        (1, 'Yokozuna'),
        (2, 'Ōzeki'),
        (3, 'Sekiwake'),
        (4, 'Komusubi'),
        (5, 'Maegashira')
    )

    MAKUUCHI_RANK_ABBREVIATIONS = {
        1: 'Y',
        2: 'O',
        3: 'S',
        4: 'K',
        5: 'M'
    }

    SIDE_CHOICES = (
        (1, 'East'),
        (2, 'West')
    )

    SIDE_ABBREVIATIONS = {
        1: 'e',
        2: 'w'
    }
    # yapf: enable

    # META
    def __str__(self):
        return f"{self.rikishi} appearance on {self.banzuke}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['banzuke', 'rikishi'], name='unique_banzuke_appearance'),
            models.UniqueConstraint(
                fields=['banzuke', 'division', 'makuuchi_rank', 'numeric_rank', 'side'], name='unique_banzuke_rank'
            )
        ]

    # MODEL FIELDS
    division = models.IntegerField(choices=DIVISION_CHOICES)
    makuuchi_rank = models.IntegerField(blank=True, null=True, choices=MAKUUCHI_RANK_CHOICES)
    numeric_rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    side = models.IntegerField(choices=SIDE_CHOICES)

    # RELATIONSHIPS
    banzuke = models.ForeignKey("banzuke.banzuke", on_delete=models.CASCADE)
    rikishi = models.ForeignKey("rikishi.rikishi", on_delete=models.CASCADE)

    # CLEANING AND VALIDATION
    def _validate_makuuchi_rank(self):
        if self.division != 1:
            self.makuuchi_rank = None
        elif self.makuuchi_rank is None:
            raise ValidationError('Must specify Makuuchi Rank for Rikishi in the top division.')

    def clean(self):
        self._validate_makuuchi_rank()

    # PROPERTIES
    @property
    def division_abbreviation(self):
        if self.division == 1:
            return self.MAKUUCHI_RANK_ABBREVIATIONS[self.makuuchi_rank]
        else:
            return self.DIVISION_ABBREVIATIONS[self.division]

    @property
    def side_abbreviation(self):
        return self.SIDE_ABBREVIATIONS[self.side]

    @property
    def rank_short(self):
        return f"{self.division_abbreviation}{self.numeric_rank}{self.side_abbreviation}"

    @property
    def rank_full(self):
        rank = self.get_makuuchi_rank_display() if self.division == 1 else self.get_division_display()
        return f"{rank} {self.numeric_rank} {self.get_side_display()}"

    @property
    def absolute_rank(self):
        """
        Returns an absolute rank for the banzuke appearance
        (ie, ignoring divisions, sanyaku and sides, if you put all the rikishi
        in a banzuke in a list from highest to lowest rank, where would this
        banzuke appearance fall on that list)
        """
        return self.banzuke.get_flat_banzuke_list().index(self) + 1

    # METHODS
    def difference_in_rank_from(self, other_appearance):
        """
        Compares the calling BanzukeAppearance's absolute rank to that of another BanzukeAppearance.

        The returned integer is the difference in rank starting at the *argument* BanzukeAppearance.
        So if the calling BanzukeAppearance is 5 ranks higher than the argument, the method will
        return *positive* 5. If the calling BanzukeAppearance is 5 ranks lower, it will return -5.

        Absolute rank is used for comparison, so that the method can be used to compare ranks
        across different banzuke as well as within one.
        This may lead to different ranks being returned as equal. For example: the lowest ranked
        Rikishi in the Makuuchi division of a banzuke may be ranked as as "low" as M18 or
        arbitrarily high (M14 in Nov 2020, for example), but will always be the 42nd highest
        Rikishi on the Banzuke, so the ranks are equivalent.

        The returned value is divided by 2 to account for side as a half-rank.
        So M2e is 0.5 ranks higher than M2w and 0.5 ranks lower than M1w.
        """
        return (other_appearance.absolute_rank - self.absolute_rank) / 2
