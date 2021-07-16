# Generated by Django 3.2.5 on 2021-07-16 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rikishi', '0005_rikishi_help_text_etc'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='heya',
            constraint=models.UniqueConstraint(condition=models.Q(('is_active', True)), fields=('name',), name='unique_name_for_active_heya'),
        ),
    ]
