import pytest

from rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestShusshin:
    def test_shusshin_model_fields(self):
        shusshin = Shusshin.objects.get(id=1)
        assert shusshin.town == "sapporo"
        assert shusshin.prefecture == "hokkaido"
        assert shusshin.country == "JP"
