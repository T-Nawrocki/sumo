from django.apps import AppConfig


class BanzukeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sumo.banzuke'

    def ready(self):
        from sumo.banzuke.models import banzuke, banzuke_appearance
