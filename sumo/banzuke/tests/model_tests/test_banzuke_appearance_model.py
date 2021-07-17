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

    # META
    def test_string_representation(self, banzuke_appearance):
        assert str(banzuke_appearance) == "Hakuho Sho appearance on Banzuke for Basho object (1)"

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

    # PROPERTIES
    def test_division_abbreviation_for_makuuchi(self, banzuke_appearance):
        assert banzuke_appearance.division_abbreviation == 'Y'
        banzuke_appearance.makuuchi_rank = 2
        assert banzuke_appearance.division_abbreviation == 'O'
        banzuke_appearance.makuuchi_rank = 3
        assert banzuke_appearance.division_abbreviation == 'S'
        banzuke_appearance.makuuchi_rank = 4
        assert banzuke_appearance.division_abbreviation == 'K'
        banzuke_appearance.makuuchi_rank = 5
        assert banzuke_appearance.division_abbreviation == 'M'

    def test_division_abbreviation_for_lower_divisions(self, banzuke_appearance):
        banzuke_appearance.division = 2
        assert banzuke_appearance.division_abbreviation == 'J'
        banzuke_appearance.division = 3
        assert banzuke_appearance.division_abbreviation == 'Ms'
        banzuke_appearance.division = 4
        assert banzuke_appearance.division_abbreviation == 'Sd'
        banzuke_appearance.division = 5
        assert banzuke_appearance.division_abbreviation == 'Jd'
        banzuke_appearance.division = 6
        assert banzuke_appearance.division_abbreviation == 'Jk'

    def test_side_abbreviations(self, banzuke_appearance):
        assert banzuke_appearance.side_abbreviation == 'e'
        banzuke_appearance.side = 2
        assert banzuke_appearance.side_abbreviation == 'w'

    def test_can_get_short_rank(self, banzuke_appearance):
        assert banzuke_appearance.rank_short == "Y1e"

    def test_can_get_full_rank(self, banzuke_appearance):
        assert banzuke_appearance.rank_full == "Yokozuna 1 East"
        banzuke_appearance.division = 3
        banzuke_appearance.side = 2
        assert banzuke_appearance.rank_full == "Makushita 1 West"
