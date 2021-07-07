from sumo.common import utils


class TestUtils:
    def test_choices_as_dict(self):
        choice_tuple = (
            (1, 'a'),
            (2, 'b'),
            (3, 'c')
        )
        assert utils.choices_as_dict(choice_tuple) == {
            1: 'a',
            2: 'b',
            3: 'c'
        }
