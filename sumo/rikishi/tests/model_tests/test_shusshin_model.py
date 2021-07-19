import pytest
from django.core.exceptions import ValidationError

from sumo.rikishi.models.rikishi import Rikishi
from sumo.rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestShusshin:

    @pytest.fixture(scope='function')
    def hokkaido(self):
        return Shusshin.objects.get(id=2)

    # META
    def test_string_representation(self, hokkaido):
        assert str(hokkaido) == "Hokkaidō"
        hokkaido.prefecture = "shimane"
        assert str(hokkaido) == "Shimane-ken"
        hokkaido.prefecture = None
        hokkaido.country = "MN"
        assert str(hokkaido) == "Mongolia"

    # MODEL FIELDS
    def test_basic_shusshin_model_fields(self, hokkaido):
        assert hokkaido.town == "sapporo"
        assert hokkaido.prefecture == "hokkaido"
        assert hokkaido.country == "JP"

    def test_heya_has_rikishi_set(self, hokkaido):
        rikishi = Rikishi.objects.get(id=42)
        assert rikishi in hokkaido.rikishi_set.all()

    # CLEANING
    def test_cannot_create_shusshin_with_invalid_country(self):
        shusshin = Shusshin(town='realtown', country='legitimateland')
        with pytest.raises(ValidationError) as excinfo:
            shusshin.save()
        assert "Value 'legitimateland' is not a valid choice." in str(excinfo.value)

    def test_foreign_shusshin_cannot_have_prefecture(self):
        shusshin = Shusshin(town='edinburgh', prefecture='midlothian', country='GB')
        with pytest.raises(ValidationError) as excinfo:
            shusshin.save()
        assert 'Foreign Shusshin cannot have a prefecture.' in str(excinfo.value)

    def test_japanese_shusshin_must_have_prefecture(self):
        shusshin = Shusshin(town='tokyo', country='JP')
        with pytest.raises(ValidationError) as excinfo:
            shusshin.save()
        assert 'Shusshin in Japan must specify a prefecture.' in str(excinfo.value)

    def test_cannot_create_shusshin_with_invalid_prefecture(self):
        shusshin = Shusshin(town='edinburgh', prefecture='midlothian', country='JP')
        with pytest.raises(ValidationError) as excinfo:
            shusshin.save()
        assert "Value 'midlothian' is not a valid choice." in str(excinfo.value)
