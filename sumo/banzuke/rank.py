# yapf: disable
DIVISIONS = (
    (1, 'Makuuchi', ''),
    (2, 'Jūryō', 'J'),
    (3, 'Makushita', 'Ms'),
    (4, 'Sandanme', 'Sd'),
    (5, 'Jonidan', 'Jd'),
    (6, 'Jonokuchi', 'Jk')
)

MAKUUCHI = (
    (1, 'Yokozuna', 'Y'),
    (2, 'Ōzeki', 'O'),
    (3, 'Sekiwake', 'S'),
    (4, 'Komusubi', 'K'),
    (5, 'Maegashira', 'M')
)

SIDES = ((1, 'East', 'E'), (2, 'West', 'W'))
# yapf: enable


def choices_from(tuple):
    return [(element[0], element[1]) for element in tuple]


def division_choices():
    return choices_from(DIVISIONS)


def makuuchi_rank_choices():
    return choices_from(MAKUUCHI)


def side_choices():
    return choices_from(SIDES)
