import json
from importlib import import_module
from typing import Dict, Optional

from pysm import State, StateMachine


class FSMBuilder:
    """
    A class to build a Finite State Machine (FSM) based on a JSON schema.

    Attributes:
        enter_methods_path (str): The path to the enter methods module.
        conditions_path (str): The path to the conditions module.
        sm (StateMachine): The state machine object being constructed.
        states_to_apply (dict): A dictionary to store states that are already added to the FSM.

    Methods:
        __call__(file_path): Build the FSM based on the logic in the JSON file provided in the file path.
        _build_fsm(current_state, previous_state): Recursive method to build the FSM from a given state.
        _get_fsm_layout(file_path): Return the FSM layout from the JSON file.
        _build_link_to_top_level_state(current_state, previous_state): Build links to top-level states.
        _build_top_level_state(current_state): Build top-level states without conditions to enter.
        _build_default_node(current_state, previous_state): Build default nodes with conditions and actions.
        _get_name(payload): Get the name of the current state from the payload.
    """
    def __init__(
        self,
        enter_methods_path: str,
        conditions_path: str
    ) -> None:
        self.sm = StateMachine("LIMA")
        self.states_to_apply = dict()
        self.enter_methods = enter_methods_path
        self.conditions = conditions_path

    def __call__(self, file_path: str = "module_schema/bgcheck.json") -> StateMachine:
        """
        Build fsm according to the logic in the json file.
        """
        fsm_tree_layout = self._get_fsm_layout(file_path)

        for state in fsm_tree_layout:
            """
            Loop through all top level states.
            """
            self._build_fsm(state)

        return self.sm

    def _build_fsm(self, current_state: Dict[str, str], previous_state: Optional[State] = None):
        name = current_state.get("name")
        if name is None:
            return

        is_state_is_already_added = name in self.states_to_apply

        if name.startswith("@"):
            self._build_link_to_top_level_state(
                current_state,
                previous_state
            )
        elif is_state_is_already_added:
            self._build_top_level_state(
                current_state
            )
        else:
            self._build_default_node(
                current_state,
                previous_state
            )

        return self.sm

    def _get_fsm_layout(self, file_path: str) -> Dict[str, str]:
        """
        Return layout for the fsm.
        """
        with open(file_path) as json_obj:
            fsm_layout = json.load(json_obj)

        return fsm_layout

    def _build_link_to_top_level_state(
        self,
        current_state: Dict[str, str],
        previous_state: State,
    ) -> None:
        """
        Links to top level states has condition and enter function
        but no states.
        """
        name = self._get_name(current_state).replace("@", "")
        state_obj = State(name)
        is_state_already_initialized = name in self.states_to_apply

        # Handle links to top level states
        if is_state_already_initialized:
            state_obj = self.states_to_apply[name]
        else:
            self.states_to_apply[name] = state_obj
            self.sm.add_state(state_obj)

        condition_name = current_state.get("condition")
        action_name = current_state.get("enter")

        # Import condition for entering to the state
        condition = getattr(import_module(self.conditions), condition_name)
        # Import method that is going to be executed
        # when user enter to the state
        action = getattr(import_module(self.enter_methods), action_name)

        self.sm.add_transition(
            previous_state,
            state_obj,
            events=["sms"],
            action=action,
            condition=condition
        )

        return

    def _build_top_level_state(self, current_state: Dict[str, str]) -> None:
        """
        Top level state has no condtion to come in
        and enter method.
        """
        name = self._get_name(current_state)
        state_obj = self.states_to_apply[name]

        for state in current_state["states"]:
            self._build_fsm(state, state_obj)

    def _build_default_node(
        self,
        current_state: Dict[str, str],
        previous_state: Optional[State] = None
    ) -> None:
        name = self._get_name(current_state)
        state_obj = State(name)

        condition_name = current_state.get("condition")
        action_name = current_state.get("enter")

        # Import condition for entering to the state
        condition = getattr(import_module(self.conditions), condition_name)
        # Import method that is going to be executed
        # when user enter to the state
        action = getattr(import_module(self.enter_methods), action_name)

        if self.sm.state is None:
            self.sm.add_state(state_obj, initial=True)
            self.sm.initialize()
        else:
            self.sm.add_state(state_obj)
            if previous_state is not None:
                self.sm.add_transition(
                    previous_state,
                    state_obj,
                    events=["sms"],
                    action=action,
                    condition=condition
                )

        if current_state.get("states") is not None:
            for state in current_state["states"]:
                self._build_fsm(state, state_obj)

    def _get_name(self, payload: Dict[str, str]) -> str:
        return payload.get("name")
