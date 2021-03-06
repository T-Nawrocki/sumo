# Generated by Django 3.2.5 on 2021-07-06 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rikishi', '0004_rikishi_shikona_and_heya_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rikishi',
            name='shikona_first',
            field=models.CharField(help_text="The rikishi's ring name.", max_length=255),
        ),
        migrations.AlterField(
            model_name='rikishi',
            name='shikona_second',
            field=models.CharField(help_text="The rikishi's ring name second name.", max_length=255),
        ),
        migrations.AlterField(
            model_name='shusshin',
            name='prefecture',
            field=models.CharField(blank=True, choices=[('aichi', 'Aichi'), ('akita', 'Akita'), ('aomori', 'Aomori'), ('chiba', 'Chiba'), ('ehime', 'Ehime'), ('fukui', 'Fukui'), ('fukuoka', 'Fukuoka'), ('fukushima', 'Fukushima'), ('gifu', 'Gifu'), ('gunma', 'Gunma'), ('hiroshima', 'Hiroshima'), ('hokkaido', 'Hokkaidō'), ('hyogo', 'Hyōgo'), ('ibaraki', 'Ibaraki'), ('ishikawa', 'Ishikawa'), ('iwate', 'Iwate'), ('kagawa', 'Kagawa'), ('kagoshima', 'Kagoshima'), ('kanagawa', 'Kanagawa'), ('kochi', 'Kōchi'), ('kumamoto', 'Kumamoto'), ('kyoto', 'Kyōto'), ('mie', 'Mie'), ('miyagi', 'Miyagi'), ('miyazaki', 'Miyazaki'), ('nagano', 'Nagano'), ('nagasaki', 'Nagasaki'), ('nara', 'Nara'), ('niigata', 'Niigata'), ('oita', 'Ōita'), ('okayama', 'Okayama'), ('okinawa', 'Okinawa'), ('osaka', 'Ōsaka'), ('saga', 'Saga'), ('saitama', 'Saitama'), ('shiga', 'Shiga'), ('shimane', 'Shimane'), ('shizuoka', 'Shizuoka'), ('tochigi', 'Tochigi'), ('tokushima', 'Tokushima'), ('tokyo', 'Tōkyō'), ('tottori', 'Tottori'), ('wakayama', 'Wakayama'), ('yamagata', 'Yamagata'), ('yamaguchi', 'Yamaguchi'), ('yamanashi', 'Yamanashi')], help_text='If the Shusshin is not in Japan, prefecture must be blank.', max_length=255),
        ),
    ]
