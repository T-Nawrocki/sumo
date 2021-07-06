import pytest
from django.core.exceptions import ValidationError

from sumo.rikishi.models.heya import Heya
from sumo.rikishi.models.rikishi import Rikishi


@pytest.mark.django_db
class TestHeya:

    # MODEL FIELDS
    def test_basic_heya_model_fields(self):
        heya = Heya.objects.get(id=1)
        assert heya.name == "miyagino"
        assert heya.is_active

    # RELATIONSHIPS
    def test_heya_has_rikishi_set(self):
        heya = Heya.objects.get(id=1)
        rikishi = Rikishi.objects.get(id=1)
        assert heya.rikishi_set.first() == rikishi

    # CLEANING
    def test_name_is_cleaned_to_lowercase(self):
        heya = Heya.objects.create(name='Kise')
        assert heya.name == "kise"

    def test_cannot_create_heya_with_same_name_as_another_active_heya(self):
        heya = Heya(name='miyagino')
        with pytest.raises(ValidationError) as excinfo:
            heya.save()
        assert 'An active Heya already exists with that name.' in str(excinfo.value)

    def test_can_create_heya_with_same_name_as_inactive_heya(self):
        heya = Heya(name='araiso')
        heya.save()

    def test_can_create_inactive_heya_with_same_name_as_active_heya(self):
        heya = Heya(name='miyagino', is_active=False)
        heya.save()

    # PROPERTY
    def test_can_get_full_name(self):
        heya = Heya.objects.get(id=1)
        assert heya.full_name == "Miyagino-beya"