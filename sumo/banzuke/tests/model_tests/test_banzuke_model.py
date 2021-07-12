import pytest

from sumo.banzuke.models.banzuke import Banzuke
from sumo.basho.models.basho import Basho
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestBanzukeModel:

    # RELATIONSHIPS
    def test_has_basho(self):
        banzuke = Banzuke.objects.get(id=1)
        basho = Basho.objects.get(id=1)
        assert banzuke.basho == basho

    def test_has_competitors(self):
        banzuke = Banzuke.objects.get(id=1)
        rikishi = Rikishi.objects.get(id=1)
        assert len(banzuke.competitors.all()) == 1
        assert banzuke.competitors.first() == rikishi
