from django.apps import AppConfig


class BrokerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.broker'

    def ready(self):
        import apps.broker.signals
