from django.apps import AppConfig


class BashoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sumo.basho'

    def ready(self):
        from sumo.basho.models import basho, torikumi
        from sumo.basho.admin import basho_admin
