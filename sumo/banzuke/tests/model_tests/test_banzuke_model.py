import pytest

from sumo.banzuke.models.banzuke import Banzuke
from sumo.banzuke.models.banzuke_appearance import BanzukeAppearance
from sumo.basho.models.basho import Basho
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestBanzuke:

    @pytest.fixture(scope='function')
    def banzuke(self):
        return Banzuke.objects.get(id=1)

    # META
    def test_string_representation(self, banzuke):
        assert str(banzuke) == "Banzuke for Basho object (1)"

    # RELATIONSHIPS
    def test_has_basho(self, banzuke):
        basho = Basho.objects.get(id=1)
        assert banzuke.basho == basho

    def test_has_competitors(self, banzuke):
        rikishi = Rikishi.objects.get(id=1)
        assert len(banzuke.competitors.all()) == 70
        assert banzuke.competitors.first() == rikishi

    # METHODS
    def test_can_get_flat_banzuke_list(self, banzuke):
        flat_banzuke = banzuke.get_flat_banzuke_list()
        assert isinstance(flat_banzuke, list)
        assert len(flat_banzuke) == 70
        assert flat_banzuke[0] == BanzukeAppearance.objects.get(id=1)
        assert flat_banzuke[41] == BanzukeAppearance.objects.get(id=42)
        assert flat_banzuke[69] == BanzukeAppearance.objects.get(id=70)
