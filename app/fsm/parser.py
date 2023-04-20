import json
from importlib import import_module

from pysm import State, StateMachine


class FSMBuilder:
    def __init__(
        self,
        enter_methods_path: str,
        conditions_path: str
    ):
        self.sm = StateMachine("LIMA")
        self.states_to_apply = dict()
        self.enter_methods = enter_methods_path
        self.conditions = conditions_path

    def __call__(self, file_path: str = "module_schema/bgcheck.json"):
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

    def _build_fsm(self, current_state: dict, previous_state=None):
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

    def _get_fsm_layout(self, file_path: str) -> dict:
        """
        Return layout for the fsm.
        """
        with open(file_path) as json_obj:
            fsm_layout = json.load(json_obj)

        return fsm_layout

    def _build_link_to_top_level_state(
        self,
        current_state: dict,
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

    def _build_top_level_state(self, current_state: dict) -> None:
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
        current_state: dict,
        previous_state: State = None
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

    def _get_name(self, payload: dict):
        return payload.get("name")
