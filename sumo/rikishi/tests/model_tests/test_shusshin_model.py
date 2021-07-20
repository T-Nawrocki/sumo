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
    def test_equality(self, hokkaido):
        assert hokkaido == hokkaido
        assert hokkaido == Shusshin(town=hokkaido.town, prefecture=hokkaido.prefecture)
        assert hokkaido == Shusshin(town='different town in the same prefecture', prefecture=hokkaido.prefecture)
        assert hokkaido != Shusshin(town=hokkaido.town, prefecture='tokyo')
        assert hokkaido != Shusshin(town=hokkaido.town, country='MN')
        assert Shusshin(town='Town A', country='MN') == Shusshin(town='Town B', country='MN')

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

    # PROPERTIES
    def test_has_value(self, hokkaido):
        assert hokkaido.value == "Hokkaidō"
        hokkaido.prefecture = "shimane"
        assert hokkaido.value == "Shimane-ken"
        hokkaido.prefecture = None
        hokkaido.country = "MN"
        assert hokkaido.value == "Mongolia"

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
