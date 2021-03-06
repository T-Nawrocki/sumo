# Generated by Django 3.2.5 on 2021-07-04 19:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rikishi', '0003_change_height_and_weight_to_positive_small'),
    ]

    operations = [
        migrations.AddField(
            model_name='rikishi',
            name='heya_id_history',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='rikishi',
            name='shikona_history',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None),
        ),
    ]
