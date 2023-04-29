"""
If the condition returns a True finite state machine changes its state
according to the JSON schema.
"""
from pysm import Event, State


def fsm_was_created(state: State, event: Event):
    """
    Initial condition.
    """
    return True


def is_user_reply_yes(state: State, event: Event):
    return event.cargo.get("user_reply").lower() == "yes"


def user_reply_name(state: State, event: Event):
    user_reply = event.cargo.get("user_reply")

    if len(user_reply) != 0:
        user = event.cargo.get("user")
        user.name = user_reply
        user.save()

        return True


def is_user_reply_no(state: State, event: Event):
    return event.cargo.get("user_reply").lower() == "no"
