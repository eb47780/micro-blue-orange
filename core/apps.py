from django.apps import AppConfig

# Configuration of core app
class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Administration Core'

    def ready(self) -> None:
        return super().ready()