import pickle

from celery import shared_task
from pysm import Event

from core.models import Session


@shared_task
def change_session_state(serialized_session: dict) -> None:
    # Change session state
    session = Session.objects.get(id=serialized_session.get("pk"))
    sm = pickle.loads(session.state)
    sm.dispatch(Event("sms", user=session.user, status=1))
    session.state = pickle.dumps(sm)
    session.save()

    return "Successefully trigger changing state."
