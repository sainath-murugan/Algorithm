from django.apps import AppConfig


class Algorithm1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'algorithm_1'
    
    def ready(self):
        import algorithm_1.signals