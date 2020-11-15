from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import DelegateDirective

from skill.helper_functions import ExploreIntents
from skill.i18n.util import get_i18n


class NoIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("AMAZON.NoIntent")(handler_input):
            return True

    def handle(self, handler_input):
        intent = Intent(name="AMAZON.StopIntent")
        handler_input.response_builder.add_directive(DelegateDirective(updated_intent=intent))
        return handler_input.response_builder.response
