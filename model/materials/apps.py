from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class MaterialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'materials'

    def ready(self):
        @receiver(post_migrate)
        def init_app(sender, **kwargs):
            if sender.name == self.name:
                try:
                    from materials.tasks import setup_periodic_tasks
                    from django_celery_beat.models import IntervalSchedule
                    # IntervalSchedule이 존재하는지 확인
                    if IntervalSchedule._meta.db_table in sender.connection.introspection.table_names():
                        setup_periodic_tasks()
                except:
                    pass  # 테이블이 없으면 무시
