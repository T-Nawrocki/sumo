from sumo.common.utils import choices_as_dict

# yapf: disable
PREFECTURES = (
    ('aichi', 'Aichi'),
    ('akita', 'Akita'),
    ('aomori', 'Aomori'),
    ('chiba', 'Chiba'),
    ('ehime', 'Ehime'),
    ('fukui', 'Fukui'),
    ('fukuoka', 'Fukuoka'),
    ('fukushima', 'Fukushima'),
    ('gifu', 'Gifu'),
    ('gunma', 'Gunma'),
    ('hiroshima', 'Hiroshima'),
    ('hokkaido', 'Hokkaidō'),
    ('hyogo', 'Hyōgo'),
    ('ibaraki', 'Ibaraki'),
    ('ishikawa', 'Ishikawa'),
    ('iwate', 'Iwate'),
    ('kagawa', 'Kagawa'),
    ('kagoshima', 'Kagoshima'),
    ('kanagawa', 'Kanagawa'),
    ('kochi', 'Kōchi'),
    ('kumamoto', 'Kumamoto'),
    ('kyoto', 'Kyōto'),
    ('mie', 'Mie'),
    ('miyagi', 'Miyagi'),
    ('miyazaki', 'Miyazaki'),
    ('nagano', 'Nagano'),
    ('nagasaki', 'Nagasaki'),
    ('nara', 'Nara'),
    ('niigata', 'Niigata'),
    ('oita', 'Ōita'),
    ('okayama', 'Okayama'),
    ('okinawa', 'Okinawa'),
    ('osaka', 'Ōsaka'),
    ('saga', 'Saga'),
    ('saitama', 'Saitama'),
    ('shiga', 'Shiga'),
    ('shimane', 'Shimane'),
    ('shizuoka', 'Shizuoka'),
    ('tochigi', 'Tochigi'),
    ('tokushima', 'Tokushima'),
    ('tokyo', 'Tōkyō'),
    ('tottori', 'Tottori'),
    ('wakayama', 'Wakayama'),
    ('yamagata', 'Yamagata'),
    ('yamaguchi', 'Yamaguchi'),
    ('yamanashi', 'Yamanashi')
)

SUFFIXES = {
    'tokyo': '-to',
    'hokkaido': '',
    'osaka': '-fu',
    'kyoto': '-fu'
}
# yapf: enable


def display_name(prefecture):
    return choices_as_dict(PREFECTURES)[prefecture]


def suffix(prefecture):
    return SUFFIXES[prefecture] if prefecture in SUFFIXES else '-ken'


def full_display_name(prefecture):
    return f"{display_name(prefecture)}{suffix(prefecture)}"
