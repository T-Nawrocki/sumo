import pytest
from django.db.utils import IntegrityError

from sumo.rikishi.models.heya import Heya
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestHeya:

    @pytest.fixture(scope='function')
    def heya(self):
        return Heya.objects.get(id=1)

    # META
    def test_string_representation(self, heya):
        assert str(heya) == "Miyagino-beya"

    # MODEL FIELDS
    def test_basic_heya_model_fields(self, heya):
        assert heya.name == "miyagino"
        assert heya.is_active

    # RELATIONSHIPS
    def test_heya_has_rikishi_set(self, heya):
        rikishi = Rikishi.objects.get(id=1)
        assert heya.rikishi_set.first() == rikishi

    # CLEANING AND VALIDATION
    def test_name_is_cleaned_to_lowercase(self):
        new_heya = Heya.objects.create(name='Kise')
        assert new_heya.name == "kise"

    def test_cannot_create_heya_with_same_name_as_another_active_heya(self):
        new_heya = Heya(name='miyagino')
        with pytest.raises(IntegrityError) as excinfo:
            new_heya.save()
        assert 'duplicate key value violates unique constraint "unique_name_for_active_heya"' in str(excinfo.value)

    def test_can_create_heya_with_same_name_as_inactive_heya(self):
        new_heya = Heya(name='araiso')
        new_heya.save()

    def test_can_create_inactive_heya_with_same_name_as_active_heya(self):
        new_heya = Heya(name='miyagino', is_active=False)
        new_heya.save()

    # PROPERTIES
    def test_can_get_full_name(self, heya):
        assert heya.full_name == "Miyagino-beya"
