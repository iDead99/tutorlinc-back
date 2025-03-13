from django.apps import AppConfig


class ManageTutorlincConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_tutorlinc'

    def ready(self) -> None:
        import manage_tutorlinc.signals