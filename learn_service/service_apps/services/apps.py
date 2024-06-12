from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_apps.services'

    def ready(self):
        from ..services import signals
