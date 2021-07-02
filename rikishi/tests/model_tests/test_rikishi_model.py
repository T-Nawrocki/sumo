import datetime

import pytest

from rikishi.models.heya import Heya
from rikishi.models.rikishi import Rikishi
from rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestRikishi:
    def test_basic_rikishi_model_fields(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.name_first == "Hakuho"
        assert rikishi.name_second == "Sho"
        assert rikishi.is_active
        assert rikishi.birth_name == "Monkhbatyn Davaajargal"
        assert rikishi.date_of_birth == datetime.date(1985, 3, 11)
        assert rikishi.height == 192
        assert rikishi.weight == 158

    def test_rikishi_has_heya(self):
        rikishi = Rikishi.objects.get(id=1)
        heya = Heya.objects.get(id=1)
        assert rikishi.heya == heya

    def test_rikishi_has_shusshin(self):
        rikishi = Rikishi.objects.get(id=1)
        shusshin = Shusshin.objects.get(id=1)
        assert rikishi.shusshin == shusshin
