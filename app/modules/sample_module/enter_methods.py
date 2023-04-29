"""
Functions in this file are what is going to be executed when
finite state machine enters each state.
"""
import pickle
from datetime import datetime, timedelta
from pprint import pprint

from django.db import IntegrityError
from pysm import Event, State

from core.models import Session
# from core.twilio import send_message
from fsm.services.task import TaskCreator

from .text_store import TextStore


def get_user_phone_number(event: Event) -> str:
    """
    Helper method to get the user's phone number from the event.
    """
    return event.cargo.get("user").phone_number


def get_state_name(state: memoryview) -> str:
    """
    Helper method to get state name for the task creator.
    """
    sm = pickle.loads(state)
    return sm.state.name


def initialize(state: State, event: Event) -> None:
    return True


def ask_agree(phone_number: str) -> None:
    sms_body = TextStore.ask_agree
    pprint(sms_body)
    pprint(phone_number)
    # send_message(sms_body, phone_number)


def ask_name(state: State, event: Event):
    sms_body = TextStore.ask_name
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    # send_message(sms_body, phone_number)


def greet_user_create_task(state: State, event: Event):
    try:
        user = event.cargo.get("user")
        session = Session.objects.get(
            user=user,
            active=True
        )
        tomorrow = datetime.now() + timedelta(minutes=2)
        state_name = get_state_name(session.state)

        create_task = TaskCreator(tomorrow, session, state_name)
        create_task()

        phone_number = get_user_phone_number(event)
        sms_body = TextStore.greet_user(user.name)
        pprint(sms_body)
        pprint(phone_number)
        # send_message(sms_body, phone_number)
    except IntegrityError:
        # Don't send message for 2 time
        pass


def say_np(state: State, event: Event):
    sms_body = TextStore.say_np
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    # send_message(sms_body, phone_number)
