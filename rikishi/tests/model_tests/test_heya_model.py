import pytest

from rikishi.models.heya import Heya


@pytest.mark.django_db
class TestHeya:
    def test_heya_model_fields(self):
        heya = Heya.objects.get(id=1)
        assert heya.name == "Miyagino"
