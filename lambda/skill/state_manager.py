from ask_sdk_core.handler_input import HandlerInput

from skill.state import State
import pytz


class StateManager:
    def __init__(self, handler_input: HandlerInput):
        attrs_manager = handler_input.attributes_manager
        sess_attrs = handler_input.attributes_manager.session_attributes
        self.handler_input = handler_input
        self._timezone = pytz.timezone(sess_attrs.get("tz_database_name"))
        self._state = State(self._timezone, attrs_manager.persistent_attributes)

    @property
    def state(self):
        # type: () -> State
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def save_to_database(self):
        self.handler_input.attributes_manager.persistent_attributes = self._state.to_dict()
        self.handler_input.attributes_manager.save_persistent_attributes()
