import pickle
from datetime import datetime, timedelta
from pprint import pprint

from django.db import IntegrityError
from pysm import Event, State

from core.models import Session
from fsm.services.task import TaskCreator

from .constants import TextStore
from core.twilio import send_message


def get_user_phone_number(event: Event):
    return event.cargo.get("user").phone_number


def get_state_name(state: memoryview) -> str:
    sm = pickle.loads(state)
    return sm.state.name


def ask_agree(phone_number: str):
    sms_body = TextStore.AGREE
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def ask_name(state: State, event: Event):
    sms_body = TextStore.ASK_NAME
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


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
        send_message(sms_body, phone_number)
    except IntegrityError:
        # Don't send message for 2 time
        pass


def say_np(state: State, event: Event):
    sms_body = TextStore.NO_PROBLEM
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def init(state: State, event: Event):
    return True


def is_user_checked_sugar(state: State, event: Event):
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

        name = user.name
        phone_number = get_user_phone_number(event)
        sms_body = TextStore.is_user_checked_sugar_value(name)
        pprint(sms_body)
        pprint(phone_number)
        send_message(sms_body, phone_number)
    except IntegrityError:
        pass


def ask_measurement(state: State, event: Event):
    user = event.cargo.get("user")
    session = Session.objects.get(user=user, active=True)
    sms_body = TextStore.ask_measurement_value(
        user.name,
        session.last_user_bgcheck_value
    )
    pprint(sms_body)
    pprint(user.phone_number)
    send_message(sms_body, user.phone_number)


def ask_about_medications(state: State, event: Event):
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
        sms_body = TextStore.MEDICATIONS
        pprint(sms_body)
        pprint(phone_number)
        send_message(sms_body, phone_number)
    except IntegrityError:
        pass


def say_fantastic(state: State, event: Event):
    user = event.cargo.get("user")
    session = Session.objects.get(
        user=user,
        active=True
    )
    tomorrow = datetime.now() + timedelta(minutes=2)
    state_name = get_state_name(session.state)

    create_task = TaskCreator(tomorrow, session, state_name)
    create_task()

    sms_body = TextStore.FANTASTIC
    phone_number = get_user_phone_number(event)
    print(sms_body)
    print(phone_number)
    send_message(sms_body, phone_number)


def warn_user_about_medications(state: State, event: Event):
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

        sms_body = TextStore.WARNING
        phone_number = get_user_phone_number(event)
        pprint(sms_body)
        pprint(phone_number)
        send_message(sms_body, phone_number)
    except IntegrityError:
        pass


def ask_first_sugar(state: State, event: Event):
    sms_body = TextStore.ASK_FIRST_SUGAR
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def recheck_sugar(state: State, event: Event) -> None:
    try:
        user = event.cargo.get("user")
        session = Session.objects.get(
            user=user,
            active=True
        )
        # Increase this flag to stop the session if NO-REPLY
        # was happened for 3 times in @NOREPLY-INIT state.
        if session.stop_session_flag is not None:
            session.stop_session_flag += 1
        else:
            session.stop_session_flag = 1

        tomorrow = datetime.now() + timedelta(minutes=2)
        state_name = get_state_name(session.state)

        create_task = TaskCreator(tomorrow, session, state_name)
        create_task()

        sms_body = TextStore.recheck_sugar_value(user.name)
        phone_number = get_user_phone_number(event)
        pprint(sms_body)
        pprint(phone_number)
        send_message(sms_body, phone_number)
    except IntegrityError:
        pass


def send_understanding_message(state: State, event: Event) -> None:
    user = event.cargo.get("user")
    session = Session.objects.get(
        user=user,
        active=True
    )
    tomorrow = datetime.now() + timedelta(minutes=2)
    state_name = get_state_name(session.state)

    create_task = TaskCreator(tomorrow, session, state_name)
    create_task()
    sms_body = TextStore.UNDERSTANDING_MESSAGE_VALUE
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def compliment(state: State, event: Event) -> None:
    # TODO: create logic that takes
    # a random compliment for user
    user = event.cargo.get("user")
    session = Session.objects.get(
        user=user,
        active=True
    )
    tomorrow = datetime.now() + timedelta(minutes=2)
    state_name = get_state_name(session.state)

    create_task = TaskCreator(tomorrow, session, state_name)
    create_task()
    sms_body = "compliment"
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def very_low_bs_warning(state: State, event: Event):
    user = event.cargo.get("user")
    session = Session.objects.get(
        user=user,
        active=True
    )
    tomorrow = datetime.now() + timedelta(minutes=2)
    state_name = get_state_name(session.state)

    create_task = TaskCreator(tomorrow, session, state_name)
    create_task()

    sms_body = TextStore.very_low_bs_text_value(
        session.last_user_bgcheck_value
    )
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def low_bs_warning(state: State, event: Event):
    sms_body = TextStore.LOW_BS_TEXT_VALUE
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def slighty_bs_warning(state: State, event: Event) -> None:
    sms_body = TextStore.SLIGHTLY_HIGH_BLOOD_SUGAR
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def ask_about_meals(state: State, event: Event) -> None:
    sms_body = TextStore.HIGH_BS_LABEL
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def bs_high_message(state: State, event: Event) -> None:
    session = Session.objects.get(
        user=event.cargo.get("user"),
        active=True
    )
    sms_body = TextStore.very_high_bs_label(session.last_user_bgcheck_value)
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)


def bs_vhigh_actions(state: State, event: Event) -> None:
    sms_body = TextStore.EXTREMELY_HIGH_LABEL
    phone_number = get_user_phone_number(event)
    pprint(sms_body)
    pprint(phone_number)
    send_message(sms_body, phone_number)
