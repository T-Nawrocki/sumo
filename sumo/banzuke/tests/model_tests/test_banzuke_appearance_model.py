from django.core.exceptions import ValidationError
import pytest

from sumo.banzuke.models.banzuke import Banzuke
from sumo.banzuke.models.banzuke_appearance import BanzukeAppearance
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestBanzukeAppearance:

    # MODEL FIELDS
    def test_has_division(self):
        banzuke_appearance = BanzukeAppearance.objects.get(id=1)
        assert banzuke_appearance.division == 1

    def test_division_max_and_min(self):
        banzuke_appearance = BanzukeAppearance(rikishi_id=2, banzuke_id=1, division=0)
        with pytest.raises(ValidationError) as excinfo:
            banzuke_appearance.save()
        assert "'division': ['Ensure this value is greater than or equal to 1.']" in str(excinfo.value)

        banzuke_appearance.division = 7
        with pytest.raises(ValidationError) as excinfo:
            banzuke_appearance.save()
        assert "'division': ['Ensure this value is less than or equal to 6.']" in str(excinfo.value)

    # RELATIONSHIPS
    def test_has_banzuke(self):
        banzuke_appearance = BanzukeAppearance.objects.get(id=1)
        banzuke = Banzuke.objects.get(id=1)
        assert banzuke_appearance.banzuke == banzuke

    def test_has_rikishi(self):
        banzuke_appearance = BanzukeAppearance.objects.get(id=1)
        rikishi = Rikishi.objects.get(id=1)
        assert banzuke_appearance.rikishi == rikishi

    def test_banzuke_rikshi_pair_must_be_unique(self):
        rikishi = Rikishi.objects.get(id=1)
        banzuke = Banzuke.objects.get(id=1)

        with pytest.raises(ValidationError) as excinfo:
            BanzukeAppearance.objects.create(rikishi=rikishi, banzuke=banzuke, division=1)
        assert "'Banzuke appearance with this Banzuke and Rikishi already exists.'" in str(excinfo.value)
