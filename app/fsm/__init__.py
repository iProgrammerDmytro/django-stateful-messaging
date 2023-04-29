# from pysm import Event, State, StateMachine

# from modules.sample.enter_methods import ask_agree

# if __name__ == "__main__":
#     initial = State("initial")
#     optin = State("optin")

#     sm = StateMachine("sm")
#     sm.add_state(initial, initial=True)
#     sm.add_state(optin)
#     sm.add_transition(
#         initial,
#         optin,
#         events=["sms"],
#         action=ask_agree,
#         condition=lambda s, e: e.cargo.get("sms") == "yes"
#     )
#     sm.initialize()
#     sm.add_transition(
#         initial,
#         optin,
#         events=["sms"],
#         action=ask_agree,
#         condition=lambda s, e: e.cargo.get("sms") == "yes"
#     )
#     sm.dispatch(Event("sms", sms="no"))
#     sm.state

#     sm.dispatch(Event("sms", sms="yes"))
