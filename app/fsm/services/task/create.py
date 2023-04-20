from datetime import datetime

from django.core import serializers
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from core.models import Session
from fsm.bgcheck.constants import TextStore


class TaskCreator:
    def __init__(
        self,
        date: datetime,
        session: Session,
        state_name: str
    ):
        self.date = date
        self.session = session
        self.state_name = state_name

    def __call__(self):
        task_name = TextStore.get_task_name(self.state_name, self.session.id)
        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=self.date.hour,
            minute=self.date.minute
        )
        serialized_session = serializers.serialize("json", [self.session, ])
        PeriodicTask.objects.create(
            crontab=schedule,
            name=task_name,
            task="core.tasks.change_session_state",
            args=serialized_session
        )
