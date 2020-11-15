from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from skill.i18n.util import get_i18n


class LearnMoreIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("LearnMoreIntent")(handler_input):
            return True

    def handle(self, handler_input):
        i18n = get_i18n(handler_input)
        return handler_input.response_builder.speak(i18n.LEARN_MORE).set_should_end_session(True).response
