from django.apps import AppConfig


class ThresholdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'threshold'

    def ready(self):
        import threshold.signals