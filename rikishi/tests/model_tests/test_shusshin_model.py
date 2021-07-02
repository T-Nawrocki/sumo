import pytest

from rikishi.models.rikishi import Rikishi
from rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestShusshin:
    def test_basic_shusshin_model_fields(self):
        shusshin = Shusshin.objects.get(id=1)
        assert shusshin.town == "sapporo"
        assert shusshin.prefecture == "hokkaido"
        assert shusshin.country == "JP"

    def test_heya_has_rikishi_set(self):
        shusshin = Shusshin.objects.get(id=1)
        rikishi = Rikishi.objects.get(id=1)
        assert shusshin.rikishi_set.first() == rikishi
