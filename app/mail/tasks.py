from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_email():
    template = render_to_string(
        "mail/email_template.html",
        {"name": "Dmytro"}
    )

    email = EmailMessage(
        "subject",
        "body",
        settings.EMAIL_HOST_USER,
        ["davashchenasrat@gmail.com"],
    )
    email.fail_silently = False
    email.send()

    return template
