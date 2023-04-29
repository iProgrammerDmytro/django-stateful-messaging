import uuid


class TextStore:
    VERY_LOW_BS_VALUE=54
    LOW_BS_VALUE=70
    SLIGHTLY_BS_VALUE=130
    HIGH_BS_VALUE=180
    VERY_HIGH_BS_VALUE=250
    EXTREMELY_HIGH_VALUE=350
    AGREE="Do you agree and opt-in to the NGHS SMS diabetes monitoring program?"
    ASK_NAME="Great! Thank you for being a part of our program to help monitor your diabetes. What is your name?"

    @staticmethod
    def greet_user(name: str) -> str:
        return f"Welcome {name}. You will start to get your first message to check your blood sugar tomorrow."

    NO_PROBLEM="No problem. Thank you for considering our project."

    @staticmethod
    def is_user_checked_sugar_value(name: str) -> str:
        return f"Howdy {name}! Were you able to check to check your blood sugar today?"

    @staticmethod
    def ask_measurement_value(name: str, last_bgcheck: int) -> str:
        return f"Hi {name}. {last_bgcheck} What was your first blood sugar measurement today?"

    MEDICATIONS="Checking your blood sugar is an important part of managing your diabetes. Were you able to get your medications?"
    FANTASTIC="Fantastic! I will check back tomorrow to see what your blood sugar reading."
    WARNING="Taking your mediation is also a very important part of managing diabetes. I will check back tomorrrow to see if you've made any progress."
    ASK_FIRST_SUGAR="Off to a great start! What was your was your first fasting blood sugar today?"

    @staticmethod
    def get_task_name(current_state: str, session_id: int) -> str:
        return f"ID: {uuid.uuid4()}. Trigger change from state {current_state} change for session {session_id}."

    @staticmethod
    def recheck_sugar_value(user_name: str) -> str:
        return f"Hey {user_name}. I hope you are having a great day. I just wanted to reach back and check to see how you're doing. Have you been able to check your blood sugar?"

    UNDERSTANDING_MESSAGE_VALUE="It can be hard sometimes..."

    @staticmethod
    def very_low_bs_text_value(bs_value: int):
        return f"Your blood sugar {bs_value} is very low and dangerous. You should immediately have something with sugar or juice. Please your health care provider immediately ..."

    LOW_BS_TEXT_VALUE="Your blood sugar is too low. You should have some juice or sweet beverage and recheck your blood sugar"
    SLIGHTLY_HIGH_BLOOD_SUGAR="Remember your target for your fasting blood sugar target is between 70-130. This value can be higher if you eat before checking your blood sugar."
    HIGH_BS_LABEL="Was this your blood sugar before meals?"

    @staticmethod
    def very_high_bs_label(bs: int) -> str:
        return f"{bs} is above your goal to maintain good control of your diabetes. "

    EXTREMELY_HIGH_LABEL="Your blood sugar is at a very high..."
