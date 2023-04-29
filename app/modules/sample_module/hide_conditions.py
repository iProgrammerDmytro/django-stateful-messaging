from pysm import Event, State

from core.models import Session

from .constants import TextStore


# def is_user_reply_yes(state: State, event: Event):
#     return event.cargo.get("user_reply").lower() == "yes"


# def user_reply_name(state: State, event: Event):
#     user_reply = event.cargo.get("user_reply")

#     if len(user_reply) != 0:
#         user = event.cargo.get("user")
#         user.name = user_reply
#         user.save()

#         return True


# def is_user_reply_no(state: State, event: Event):
#     return event.cargo.get("user_reply").lower() == "no"


# def get_smth_from_user(state: State, event: Event):
#     return event.cargo.get("user_reply") is not None


# def user_reply_bs(state: State, event: Event):
#     user_reply = event.cargo.get("user_reply")
#     user = event.cargo.get("user")
#     if len(user_reply) != 0:
#         try:
#             bg = int(user_reply)
#         except ValueError:
#             pass
#         else:
#             s = Session.objects.get(
#                 user=user,
#                 active=True
#             )
#             s.last_user_bgcheck_value = bg
#             s.save()
#             return True


# TODO: make this functions work
# with the celery + celery beat scheduler
def trigger_noreply_init_in_24_hrs(state: State, event: Event):
    return True


def trigger_bgcheck_in_24_hrs(state: State, event: Event):
    return True


def init(state: State, event: Event):
    return True


def task_was_created(state: State, event: Event) -> bool:
    return bool(event.cargo.get("status"))


def bs_lte_54(state: State, event: Event) -> bool:
    user_reply = event.cargo.get("user_reply")
    user = event.cargo.get("user")
    try:
        bg = int(user_reply)
    except ValueError:
        pass
    else:
        s = Session.objects.get(
            user=user,
            active=True
        )
        s.last_user_bgcheck_value = bg
        s.save()
        return bg < TextStore.VERY_LOW_BS_VALUE


def bs_lte_70_gte_54(state: State, event: Event) -> bool:
    user_reply = event.cargo.get("user_reply")
    user = event.cargo.get("user")
    try:
        bg = int(user_reply)
    except ValueError:
        pass
    else:
        s = Session.objects.get(
            user=user,
            active=True
        )
        s.last_user_bgcheck_value = bg
        s.save()
        return TextStore.VERY_LOW_BS_VALUE < bg < TextStore.LOW_BS_VALUE


def bs_lte_130_gte_70(state: State, event: Event) -> bool:
    user_reply = event.cargo.get("user_reply")
    user = event.cargo.get("user")
    try:
        bg = int(user_reply)
    except ValueError:
        pass
    else:
        s = Session.objects.get(
            user=user,
            active=True
        )
        s.last_user_bgcheck_value = bg
        s.save()
        return TextStore.LOW_BS_VALUE < bg < TextStore.SLIGHTLY_BS_VALUE


def bs_lte_180_gte_130(state: State, event: Event) -> bool:
    user_reply = event.cargo.get("user_reply")
    user = event.cargo.get("user")
    try:
        bg = int(user_reply)
    except ValueError:
        pass
    else:
        s = Session.objects.get(
            user=user,
            active=True
        )
        s.last_user_bgcheck_value = bg
        s.save()
        return TextStore.SLIGHTLY_BS_VALUE < bg < TextStore.HIGH_BS_VALUE


def bs_gte_180(state: State, event: Event) -> bool:
    user_reply = event.cargo.get("user_reply")
    user = event.cargo.get("user")
    try:
        bg = int(user_reply)
    except ValueError:
        pass
    else:
        s = Session.objects.get(
            user=user,
            active=True
        )
        s.last_user_bgcheck_value = bg
        s.save()

    return s.last_user_bgcheck_value > TextStore.HIGH_BS_VALUE


def bs_lte_250_gte_180(state: State, event: Event) -> None:
    user = event.cargo.get("user")
    session = Session.objects.get(
        user=user,
        active=True
    )

    return TextStore.HIGH_BS_VALUE \
        < session.last_user_bgcheck_value < TextStore.VERY_HIGH_BS_VALUE


def bs_gte_250(state: State, event: Event) -> None:
    user = event.cargo.get("user")
    session = Session.objects.get(
        user=user,
        active=True
    )

    return TextStore.VERY_HIGH_BS_VALUE \
        < session.last_user_bgcheck_value < TextStore.EXTREMELY_HIGH_VALUE
