from django.apps import AppConfig


class ManageAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_app'
    def ready(self):
        from manage_app import signals