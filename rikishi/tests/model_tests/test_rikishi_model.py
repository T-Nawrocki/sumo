import datetime

import pytest

from rikishi.models.heya import Heya
from rikishi.models.rikishi import Rikishi
from rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestRikishiManager:
    def test_can_get_active_rikishi(self):
        rikishi = Rikishi.objects.get(id=1)
        active = Rikishi.objects.active()
        assert active.first() == rikishi

    def test_can_get_inactive_rikishi(self):
        rikishi = Rikishi.objects.get(id=2)
        inactive = Rikishi.objects.inactive()
        assert inactive.first() == rikishi


@pytest.mark.django_db
class TestRikishi:

    # MODEL FIELDS
    def test_basic_rikishi_model_fields(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.name_first == "Hakuho"
        assert rikishi.name_second == "Sho"
        assert rikishi.is_active
        assert rikishi.birth_name == "Monkhbatyn Davaajargal"
        assert rikishi.date_of_birth == datetime.date(1985, 3, 11)
        assert rikishi.height == 192
        assert rikishi.weight == 158

    # RELATIONSHIPS
    def test_rikishi_has_heya(self):
        rikishi = Rikishi.objects.get(id=1)
        heya = Heya.objects.get(id=1)
        assert rikishi.heya == heya

    def test_rikishi_has_shusshin(self):
        rikishi = Rikishi.objects.get(id=1)
        shusshin = Shusshin.objects.get(id=1)
        assert rikishi.shusshin == shusshin

    # PROPERTIES
    def test_can_get_age(self):
        rikishi = Rikishi.objects.get(id=1)
        today = datetime.date.today()
        upcoming_birthday = ((today.month, today.day) < (rikishi.date_of_birth.month, rikishi.date_of_birth.day))
        expected_age = today.year - rikishi.date_of_birth.year - upcoming_birthday
        assert rikishi.age == expected_age
