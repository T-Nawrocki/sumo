import datetime

import pytest

from rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestRikishi:
    def test_rikishi_model_fields(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.name_first == "Hakuho"
        assert rikishi.name_second == "Sho"
        assert rikishi.is_active
        assert rikishi.birth_name == "Monkhbatyn Davaajargal"
        assert rikishi.date_of_birth == datetime.date(1985, 3, 11)
        assert rikishi.height == 192
        assert rikishi.weight == 158
