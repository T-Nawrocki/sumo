from django.core.exceptions import ValidationError
import pytest

from sumo.banzuke.models.banzuke import Banzuke
from sumo.banzuke.models.banzuke_appearance import BanzukeAppearance
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestBanzukeAppearance:

    @pytest.fixture(scope='function')
    def banzuke_appearance(self):
        return BanzukeAppearance.objects.get(id=1)

    # MODEL FIELDS
    def test_has_division(self, banzuke_appearance):
        assert banzuke_appearance.division == 1

    def test_has_makuuchi_rank(self, banzuke_appearance):
        assert banzuke_appearance.makuuchi_rank == 1

    def test_makuuchi_rank_can_be_none(self, banzuke_appearance):
        banzuke_appearance.makuuchi_rank = None
        banzuke_appearance.save()

    def test_has_numeric_rank(self, banzuke_appearance):
        assert banzuke_appearance.numeric_rank == 1

    def test_numeric_rank_max_and_min(self, banzuke_appearance):
        banzuke_appearance.numeric_rank = 0
        with pytest.raises(ValidationError) as excinfo:
            banzuke_appearance.save()
        assert "numeric_rank': ['Ensure this value is greater than or equal to 1.']" in str(excinfo.value)

        banzuke_appearance.numeric_rank = 151
        with pytest.raises(ValidationError) as excinfo:
            banzuke_appearance.save()
        assert "numeric_rank': ['Ensure this value is less than or equal to 150.']" in str(excinfo.value)

    def test_has_side(self, banzuke_appearance):
        assert banzuke_appearance.side == 1

    # RELATIONSHIPS
    def test_has_banzuke(self, banzuke_appearance):
        banzuke = Banzuke.objects.get(id=1)
        assert banzuke_appearance.banzuke == banzuke

    def test_has_rikishi(self, banzuke_appearance):
        rikishi = Rikishi.objects.get(id=1)
        assert banzuke_appearance.rikishi == rikishi

    def test_banzuke_rikshi_pair_must_be_unique(self):
        rikishi = Rikishi.objects.get(id=1)
        banzuke = Banzuke.objects.get(id=1)

        with pytest.raises(ValidationError) as excinfo:
            BanzukeAppearance.objects.create(rikishi=rikishi, banzuke=banzuke, division=1, numeric_rank=1)
        assert "'Banzuke appearance with this Banzuke and Rikishi already exists.'" in str(excinfo.value)
