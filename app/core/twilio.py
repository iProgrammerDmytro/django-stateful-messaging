from django.conf import settings
from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER


def send_message(sms_body: str, phone_number: str) -> MessageInstance:
    client = Client(ACCOUNT_SID, TWILIO_TOKEN)
    message = client.messages.create(
                                    body=sms_body,
                                    from_=TWILIO_PHONE_NUMBER,
                                    to=phone_number
    )
    return message
