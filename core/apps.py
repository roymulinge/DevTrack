from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Shared'
    
    def ready(self):
      print("Core app is ready!")
      