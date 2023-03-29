from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Administration Core'

    def ready(self) -> None:
        return super().ready()