from django.apps import AppConfig


class RikishiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sumo.rikishi'

    def ready(self):
        from sumo.rikishi.models import heya, rikishi, shusshin
        from sumo.rikishi.admin import heya_admin, rikishi_admin, shusshin_admin
