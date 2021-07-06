from sumo.geography import prefectures


class TestPrefectures:
    def test_can_get_display_name(self):
        assert prefectures.display_name('tokyo') == 'Tōkyō'

    def test_can_get_suffix(self):
        assert prefectures.suffix('tokyo') == '-to'
        assert prefectures.suffix('hokkaido') == ''
        assert prefectures.suffix('osaka') == '-fu'
        assert prefectures.suffix('shimane') == '-ken'

    def test_can_get_full_display_name(self):
        assert prefectures.full_display_name('tokyo') == 'Tōkyō-to'
