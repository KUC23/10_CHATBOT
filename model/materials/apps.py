from django.apps import AppConfig

class MaterialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'materials'

    def ready(self):
        # from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from materials.tasks import setup_periodic_tasks

        setup_periodic_tasks()
