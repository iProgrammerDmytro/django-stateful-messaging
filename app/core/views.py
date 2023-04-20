import pickle

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pysm import Event

from core.models import Session


@csrf_exempt
def user_reply(request):
    """
    Endpoint for response from user via twilio webhooks.
    """
    data = None
    if getattr(request, "method") == "POST":
        data = request.POST

        # Get data from the user
        user_phone_number = data.get("From")
        user_reply = data.get("Body")

        # get the models instances
        user = get_user_model().objects.get(
            phone_number=user_phone_number
        )
        session = Session.objects.get(
            user=user,
            active=True
        )

        # get the final state machine
        sm = pickle.loads(session.state)

        # put the user_reply into the final state machine
        # to potentially trigger the event.
        sm.dispatch(Event("sms", user_reply=user_reply, user=user))

        # update state in the session
        binary_sm = pickle.dumps(sm)
        session.state = binary_sm
        session.save()

        return HttpResponse(data)

    return HttpResponse(data)
