from django.core.exceptions import ValidationError
import pytest

from sumo.basho.models.basho import Basho
from sumo.basho.models.torikumi import Torikumi


@pytest.mark.django_db
class TestTorikumiModel:

    @pytest.fixture(scope='function')
    def nagoya_day_1(self):
        return Torikumi.objects.get(id=1)

    # META
    def test_string_representation(self, nagoya_day_1):
        assert str(nagoya_day_1) == "Torikumi for Basho object (1) day 1"

    # MODEL FIELDS
    def test_has_day(self, nagoya_day_1):
        assert nagoya_day_1.day == 1

    # RELATIONSHIPS
    def test_has_basho(self, nagoya_day_1):
        assert nagoya_day_1.basho == Basho.objects.get(id=1)

    # CLEANING AND VALIDATION
    def test_day_max_and_min(self, nagoya_day_1):
        nagoya_day_1.day = 0
        with pytest.raises(ValidationError) as excinfo:
            nagoya_day_1.save()
        assert "'day': ['Ensure this value is greater than or equal to 1.']" in str(excinfo.value)

        nagoya_day_1.day = 16
        with pytest.raises(ValidationError) as excinfo:
            nagoya_day_1.save()
        assert "'day': ['Ensure this value is less than or equal to 15.']" in str(excinfo.value)
