import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from sumo.rikishi.models.heya import Heya
from sumo.rikishi.models.rikishi import Rikishi
from sumo.rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestRikishiManager:

    def test_can_get_active_rikishi(self):
        rikishi = Rikishi.objects.get(id=1)
        active = Rikishi.objects.active()
        assert active.first() == rikishi

    def test_can_get_inactive_rikishi(self):
        rikishi = Rikishi.objects.get(id=71)
        inactive = Rikishi.objects.inactive()
        assert inactive.first() == rikishi


@pytest.mark.django_db
class TestRikishi:

    @pytest.fixture(scope='function')
    def hakuho(self):
        return Rikishi.objects.get(id=1)

    @pytest.fixture(scope='function')
    def harumafuji(self):
        return Rikishi.objects.get(id=71)

    # META
    def test_string_representation(self, hakuho):
        assert str(hakuho) == 'Hakuho Sho'

    # BASIC MODEL FIELDS
    def test_basic_rikishi_model_fields(self, hakuho):
        assert hakuho.shikona_first == "hakuho"
        assert hakuho.shikona_second == "sho"
        assert hakuho.is_active
        assert hakuho.birth_name == "Mönkhbat Davaajargal"
        assert hakuho.date_of_birth == datetime.date(1985, 3, 11)
        assert hakuho.height == 192
        assert hakuho.weight == 152

    # HISTORY FIELDS
    def test_has_shikona_history(self, harumafuji):
        assert harumafuji.shikona_history == ['ama kohei', 'harumafuji kohei']

    def test_default_shikona_history_on_creation(self):
        rikishi = Rikishi.objects.create(
            shikona_first="New",
            shikona_second="Rikishi",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        assert rikishi.shikona_history == ["new rikishi"]

    def test_shikona_history_updates_when_name_is_changed(self, hakuho):
        assert hakuho.shikona_history == ['hakuho sho']
        hakuho.shikona_first = "hokuha"
        hakuho.save()
        assert hakuho.shikona_history == ['hakuho sho', 'hokuha sho']

    def test_shikona_history_does_not_update_if_name_has_not_changed(self, hakuho):
        assert hakuho.shikona_history == ['hakuho sho']
        hakuho.is_active = False
        hakuho.save()
        assert hakuho.shikona_history == ['hakuho sho']

    def test_has_heya_id_history(self, harumafuji):
        assert harumafuji.heya_id_history == [32, 2]

    def test_default_heya_id_history_on_rikishi_creation(self):
        rikishi = Rikishi.objects.create(
            shikona_first="New",
            shikona_second="Rikishi",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        assert rikishi.heya_id_history == [1]

    def test_heya_id_history_updates_when_heya_is_changed(self, hakuho):
        assert hakuho.heya_id_history == [1]
        hakuho.heya_id = 2
        hakuho.save()
        assert hakuho.heya_id_history == [1, 2]

    def test_heya_id_history_does_not_update_if_heya_has_not_changed(self, hakuho):
        assert hakuho.heya_id_history == [1]
        hakuho.is_active = False
        hakuho.save()
        assert hakuho.heya_id_history == [1]

    # RELATIONSHIPS
    def test_rikishi_has_heya(self, hakuho):
        heya = Heya.objects.get(id=1)
        assert hakuho.heya == heya

    def test_rikishi_has_shusshin(self, hakuho):
        shusshin = Shusshin.objects.get(id=1)
        assert hakuho.shusshin == shusshin

    # CLEANING AND VALIDATION
    def test_rikishi_name_is_cleaned_to_lowercase(self):
        rikishi = Rikishi.objects.create(
            shikona_first="New",
            shikona_second="Rikishi",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        assert rikishi.shikona_first == "new"
        assert rikishi.shikona_second == "rikishi"

    def test_cannot_create_rikishi_with_same_name_as_another_active_rikishi(self):
        rikishi = Rikishi(
            shikona_first="Hakuho",
            shikona_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        with pytest.raises(IntegrityError) as excinfo:
            rikishi.save()
        assert 'duplicate key value violates unique constraint "unique_shikona_for_active_rikishi"' in str(
            excinfo.value
        )

    def test_can_create_rikishi_with_same_name_as_inactive_rikishi(self):
        rikishi = Rikishi(
            shikona_first="Harumafuji",
            shikona_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        rikishi.save()

    def test_can_create_inactive_rikishi_with_non_unique_name(self):
        rikishi = Rikishi(
            shikona_first="Hakuho",
            shikona_second="Akira",
            is_active=False,
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        rikishi.save()

    def test_height_max_and_min(self, hakuho):
        hakuho.height = 149
        with pytest.raises(ValidationError) as excinfo:
            hakuho.save()
        assert "'height': ['Ensure this value is greater than or equal to 150.']" in str(excinfo.value)

        hakuho.height = 251
        with pytest.raises(ValidationError) as excinfo:
            hakuho.save()
        assert "'height': ['Ensure this value is less than or equal to 250.']" in str(excinfo.value)

    def test_weight_max_and_min(self, hakuho):
        hakuho.weight = 49
        with pytest.raises(ValidationError) as excinfo:
            hakuho.save()
        assert "'weight': ['Ensure this value is greater than or equal to 50.']" in str(excinfo.value)

        hakuho.weight = 351
        with pytest.raises(ValidationError) as excinfo:
            hakuho.save()
        assert "'weight': ['Ensure this value is less than or equal to 350.']" in str(excinfo.value)

    def test_cannot_create_rikishi_under_fifteen(self):
        today = datetime.date.today()
        five_years_ago = today - datetime.timedelta(days=5 * 365.25)
        rikishi = Rikishi(
            shikona_first="Enho",
            shikona_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=five_years_ago,
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        with pytest.raises(ValidationError) as excinfo:
            rikishi.save()
        assert 'Rikishi cannot be under 15.' in str(excinfo.value)

        fourteen_years_364_days_ago = today - datetime.timedelta(days=14 * 365.25 + 364)
        rikishi.date_of_birth = fourteen_years_364_days_ago
        with pytest.raises(ValidationError) as excinfo:
            rikishi.save()
        assert 'Rikishi cannot be under 15.' in str(excinfo.value)

    # PROPERTIES
    def test_can_get_age(self, hakuho):
        today = datetime.date.today()
        upcoming_birthday = ((today.month, today.day) < (hakuho.date_of_birth.month, hakuho.date_of_birth.day))
        expected_age = today.year - hakuho.date_of_birth.year - upcoming_birthday
        assert hakuho.age == expected_age

    def test_can_get_shikona_full(self, hakuho):
        assert hakuho.shikona_full == "hakuho sho"

    def test_can_get_shikona_display(self, hakuho):
        assert hakuho.shikona_display == "Hakuho Sho"
