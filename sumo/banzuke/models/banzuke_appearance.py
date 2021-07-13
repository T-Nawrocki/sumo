from django.db import models


class BanzukeAppearance(models.Model):
    """
    Through-model mapping the many-to-many relationship between Rikishi and Banzuke.
    Contains rank information for the Rikishi's rank on this banzuke.
    Ranks are represented as integers for easy comparison.
    """

    class Meta:
        constraints = [models.UniqueConstraint(fields=['banzuke', 'rikishi'], name='unique_banzuke_appearance')]

    banzuke = models.ForeignKey("banzuke.banzuke", on_delete=models.CASCADE)
    rikishi = models.ForeignKey("rikishi.rikishi", on_delete=models.CASCADE)
