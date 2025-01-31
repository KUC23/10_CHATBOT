from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')

app = Celery('final_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# @app.task(bind=True) 디버깅 코드, 필요없어지면 지울것
# def debug_task(self):
#     print(f'Request: {self.request!r}')
