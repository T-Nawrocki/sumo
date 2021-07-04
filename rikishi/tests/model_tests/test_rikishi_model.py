import datetime

import pytest
from django.core.exceptions import ValidationError

from rikishi.models.heya import Heya
from rikishi.models.rikishi import Rikishi
from rikishi.models.shusshin import Shusshin


@pytest.mark.django_db
class TestRikishiManager:
    def test_can_get_active_rikishi(self):
        rikishi = Rikishi.objects.get(id=1)
        active = Rikishi.objects.active()
        assert active.first() == rikishi

    def test_can_get_inactive_rikishi(self):
        rikishi = Rikishi.objects.get(id=2)
        inactive = Rikishi.objects.inactive()
        assert inactive.first() == rikishi


@pytest.mark.django_db
class TestRikishi:

    # BASIC MODEL FIELDS
    def test_basic_rikishi_model_fields(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.name_first == "hakuho"
        assert rikishi.name_second == "sho"
        assert rikishi.is_active
        assert rikishi.birth_name == "Monkhbatyn Davaajargal"
        assert rikishi.date_of_birth == datetime.date(1985, 3, 11)
        assert rikishi.height == 192
        assert rikishi.weight == 158

    # HISTORY FIELDS
    def test_has_name_history(self):
        rikishi = Rikishi.objects.get(id=2)
        assert rikishi.name_history == ['ama kohei', 'harumafuji kohei']

    def test_default_name_history_on_creation(self):
        rikishi = Rikishi.objects.create(
            name_first="Enho",
            name_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        assert rikishi.name_history == ["enho akira"]

    def test_name_history_updates_when_name_is_changed(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.name_history == ['hakuho sho']
        rikishi.name_first = "hokuha"
        rikishi.save()
        assert rikishi.name_history == ['hakuho sho', 'hokuha sho']

    def test_name_history_does_not_update_if_name_has_not_changed(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.name_history == ['hakuho sho']
        rikishi.is_active = False
        rikishi.save()
        assert rikishi.name_history == ['hakuho sho']

    def test_has_heya_id_history(self):
        rikishi = Rikishi.objects.get(id=2)
        assert rikishi.heya_id_history == [1, 2]

    def test_default_heya_id_history_on_rikishi_creation(self):
        rikishi = Rikishi.objects.create(
            name_first="Enho",
            name_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        assert rikishi.heya_id_history == [1]

    def test_heya_id_history_updates_when_heya_is_changed(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.heya_id_history == [1]
        rikishi.heya_id = 2
        rikishi.save()
        assert rikishi.heya_id_history == [1, 2]

    def test_heya_id_history_does_not_update_if_heya_has_not_changed(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.heya_id_history == [1]
        rikishi.is_active = False
        rikishi.save()
        assert rikishi.heya_id_history == [1]

    # RELATIONSHIPS
    def test_rikishi_has_heya(self):
        rikishi = Rikishi.objects.get(id=1)
        heya = Heya.objects.get(id=1)
        assert rikishi.heya == heya

    def test_rikishi_has_shusshin(self):
        rikishi = Rikishi.objects.get(id=1)
        shusshin = Shusshin.objects.get(id=1)
        assert rikishi.shusshin == shusshin

    # CLEANING
    def test_rikishi_name_is_cleaned_to_lowercase(self):
        rikishi = Rikishi.objects.create(
            name_first="Enho",
            name_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        assert rikishi.name_first == "enho"
        assert rikishi.name_second == "akira"

    def test_cannot_create_rikishi_with_same_name_as_another_active_rikishi(self):
        rikishi = Rikishi(
            name_first="Hakuho",
            name_second="Akira",
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        with pytest.raises(ValidationError) as excinfo:
            rikishi.save()
        assert 'An active Rikishi already exists with that first name.' in str(excinfo.value)

    def test_can_create_rikishi_with_same_name_as_inactive_rikishi(self):
        rikishi = Rikishi(
            name_first="Harumafuji",
            name_second="Akira",
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
            name_first="Hakuho",
            name_second="Akira",
            is_active=False,
            birth_name="Yūya Nakamura",
            date_of_birth=datetime.date(1994, 10, 18),
            height=168,
            weight=98,
            heya_id=1,
            shusshin_id=1
        )
        rikishi.save()

    def test_cannot_create_rikishi_under_fifteen(self):
        today = datetime.date.today()
        five_years_ago = today - datetime.timedelta(days=5 * 365.25)
        rikishi = Rikishi(
            name_first="Enho",
            name_second="Akira",
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
    def test_can_get_age(self):
        rikishi = Rikishi.objects.get(id=1)
        today = datetime.date.today()
        upcoming_birthday = ((today.month, today.day) < (rikishi.date_of_birth.month, rikishi.date_of_birth.day))
        expected_age = today.year - rikishi.date_of_birth.year - upcoming_birthday
        assert rikishi.age == expected_age

    def test_can_get_full_name(self):
        rikishi = Rikishi.objects.get(id=1)
        assert rikishi.full_name == "hakuho sho"
