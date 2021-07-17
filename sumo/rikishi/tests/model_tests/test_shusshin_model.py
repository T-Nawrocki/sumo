import pytest
from django.core.exceptions import ValidationError

from sumo.rikishi.models.rikishi import Rikishi
from sumo.rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestShusshin:

    @pytest.fixture(scope='function')
    def shusshin(self):
        return Shusshin.objects.get(id=1)

    # META
    def test_string_representation(self, shusshin):
        assert str(shusshin) == "Hokkaidō"
        shusshin.prefecture = "shimane"
        assert str(shusshin) == "Shimane-ken"
        shusshin.prefecture = None
        shusshin.country = "MN"
        assert str(shusshin) == "Mongolia"

    # MODEL FIELDS
    def test_basic_shusshin_model_fields(self, shusshin):
        assert shusshin.town == "sapporo"
        assert shusshin.prefecture == "hokkaido"
        assert shusshin.country == "JP"

    def test_heya_has_rikishi_set(self, shusshin):
        rikishi = Rikishi.objects.get(id=1)
        assert shusshin.rikishi_set.first() == rikishi

    # CLEANING
    def test_cannot_create_shusshin_with_invalid_country(self):
        shusshin = Shusshin(town='realtown', country='legitimateland')
        with pytest.raises(ValidationError) as excinfo:
            shusshin.save()
        assert "Value 'legitimateland' is not a valid choice." in str(excinfo.value)

    def test_foreign_shusshin_cannot_have_prefecture(self):
        new_shusshin = Shusshin(town='edinburgh', prefecture='midlothian', country='GB')
        with pytest.raises(ValidationError) as excinfo:
            new_shusshin.save()
        assert 'Foreign Shusshin cannot have a prefecture.' in str(excinfo.value)

    def test_japanese_shusshin_must_have_prefecture(self):
        new_shusshin = Shusshin(town='tokyo', country='JP')
        with pytest.raises(ValidationError) as excinfo:
            new_shusshin.save()
        assert 'Shusshin in Japan must specify a prefecture.' in str(excinfo.value)

    def test_cannot_create_shusshin_with_invalid_prefecture(self):
        new_shusshin = Shusshin(town='edinburgh', prefecture='midlothian', country='JP')
        with pytest.raises(ValidationError) as excinfo:
            new_shusshin.save()
        assert "Value 'midlothian' is not a valid choice." in str(excinfo.value)
