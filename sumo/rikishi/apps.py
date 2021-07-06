from django.apps import AppConfig


class RikishiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sumo.rikishi'

    def ready(self):
        from sumo.rikishi.models import rikishi, heya, shusshin
