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

    # METHODS
    def is_higher_rank_than(self, other_appearance):
        """
        Compares the ranks of two BanzukeAppearance instances.
        Returns:
            * True  : if the calling instance is higher rank than the argument
            * False : if the argument is higher rank than the calling instance
            * None : if the two instances have the same rank
        
        Be careful when comparing using this function. `not banzuke_appearance.is_higher_rank_than(other_appearance)`
        will be True even if the two instances have the same rank. If in doubt, use
        `banzuke_appearance.is_higher_rank_than(other_appearance) is False` instead.

        (Remember, we're talking about a higher rank in real-terms, not numerically.
        Higher ranks are represented by lower numbers.)
        """
        if self.rank_short == other_appearance.rank_short:
            return None

        same_division = self.division == other_appearance.division
        same_makuuchi_rank = self.makuuchi_rank == other_appearance.makuuchi_rank
        same_numeric_rank = self.numeric_rank == other_appearance.numeric_rank

        if same_division and same_makuuchi_rank and same_numeric_rank:
            return self.side < other_appearance.side
        elif same_division and same_makuuchi_rank: # Also covers non-makuuchi where makuuchi_rank is None
            return self.numeric_rank < other_appearance.numeric_rank
        elif same_division and self.division == 1:
            return self.makuuchi_rank < other_appearance.makuuchi_rank
        else:
            return self.division < other_appearance.division
