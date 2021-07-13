from django.db.utils import IntegrityError
import pytest

from sumo.banzuke.models.banzuke import Banzuke
from sumo.banzuke.models.banzuke_appearance import BanzukeAppearance
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestBanzukeAppearance:

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

        with pytest.raises(IntegrityError) as excinfo:
            BanzukeAppearance.objects.create(rikishi=rikishi, banzuke=banzuke)
        assert "Key (banzuke_id, rikishi_id)=(1, 1) already exists." in str(excinfo.value)
