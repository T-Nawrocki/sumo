from sumo.banzuke import rank


class TestRank:
    def test_can_get_choices_from_tuples(self):
        divisions = [(1, 'Makuuchi'), (2, 'Jūryō'), (3, 'Makushita'), (4, 'Sandanme'), (5, 'Jonidan'), (6, 'Jonokuchi')]
        makuuchi = [(1, 'Yokozuna'), (2, 'Ōzeki'), (3, 'Sekiwake'), (4, 'Komusubi'), (5, 'Maegashira')]
        sides = [(1, 'East'), (2, 'West')]
        assert rank.choices_from(rank.DIVISIONS) == divisions
        assert rank.choices_from(rank.MAKUUCHI) == makuuchi
        assert rank.choices_from(rank.SIDES) == sides

    def test_can_get_abbreviations_from_tuples(self):
        divisions = rank.abbreviations_from(rank.DIVISIONS)
        makuuchi = rank.abbreviations_from(rank.MAKUUCHI)
        sides = rank.abbreviations_from(rank.SIDES)

        assert divisions[2] == 'J'
        assert makuuchi[1] == 'Y'
        assert sides[2] == 'W'
