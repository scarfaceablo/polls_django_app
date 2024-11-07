import os

from celery.schedules import crontab
from django.conf import settings

from celery import Celery

from polls.utils.question_generator import QuestionGenerator

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polls_django_app.settings')

app = Celery('polls_django_app')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls create_question every 10 seconds.
    sender.add_periodic_task(3600, create_question, name='add every 1 hour')


@app.task
def create_question():
    QuestionGenerator().generate_question()


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(f'django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
