import pytest

from rikishi.models.heya import Heya
from rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestHeya:
    def test_basic_heya_model_fields(self):
        heya = Heya.objects.get(id=1)
        assert heya.name == "Miyagino"
        assert heya.is_active

    def test_heya_has_rikishi_set(self):
        heya = Heya.objects.get(id=1)
        rikishi = Rikishi.objects.get(id=1)
        assert heya.rikishi_set.first() == rikishi
