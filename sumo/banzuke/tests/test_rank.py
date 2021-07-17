from sumo.banzuke import rank


class TestRank:

    def test_can_get_choices_from_tuples(self):
        assert rank.choices_from(rank.DIVISIONS) == [(1, 'Makuuchi'), (2, 'Jūryō'), (3, 'Makushita'), (4, 'Sandanme'),
                                                     (5, 'Jonidan'), (6, 'Jonokuchi')]
        assert rank.choices_from(rank.MAKUUCHI) == [(1, 'Yokozuna'), (2, 'Ōzeki'), (3, 'Sekiwake'), (4, 'Komusubi'),
                                                    (5, 'Maegashira')]
        assert rank.choices_from(rank.SIDES) == [(1, 'East'), (2, 'West')]

    def test_division_choices(self):
        assert rank.division_choices() == [(1, 'Makuuchi'), (2, 'Jūryō'), (3, 'Makushita'), (4, 'Sandanme'),
                                           (5, 'Jonidan'), (6, 'Jonokuchi')]

    def test_makuuchi_rank_choices(self):
        assert rank.makuuchi_rank_choices() == [(1, 'Yokozuna'), (2, 'Ōzeki'), (3, 'Sekiwake'), (4, 'Komusubi'),
                                                (5, 'Maegashira')]

    def test_side_choices(self):
        assert rank.side_choices() == [(1, 'East'), (2, 'West')]
