"""
Signals for the project.
"""
import pickle

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.models import Session
from modules.sample_module.enter_methods import ask_agree
from fsm.parser import FSMBuilder


@receiver(pre_save, sender=Session)
def initialize_start_attrs(sender, instance, **kwargs):
    """
    Initialize first session state.
    """
    if instance.state is None:
        instance.active = True
        build_fsm = FSMBuilder(
            "modules.sample_module.enter_methods",
            "modules.sample_module.conditions"
        )
        sm = build_fsm("modules/module_schema/sample_schema.json")

        binary_sm = pickle.dumps(sm)
        instance.state = binary_sm

    # Check if we should stop the session
    if instance.stop_session_flag == settings.NO_REPLY_MAX_VALUE:
        instance.active = False
        # TODO: create a function that will send the email


@receiver(post_save, sender=Session)
def send_start_message(sender, instance, created, **kwargs):
    """
    Send the first message.
    """
    if created:
        ask_agree(instance.user.phone_number)
