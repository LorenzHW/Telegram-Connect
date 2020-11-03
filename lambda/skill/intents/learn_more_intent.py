from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from skill.i18n.util import get_i18n


class LearnMoreIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("LearnMoreIntent")(handler_input):
            return True

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(handler_input.request_envelope.request.locale, sess_attrs.get("tz_database_name"))
        return handler_input.response_builder.speak(i18n.LEARN_MORE).set_should_end_session(True).response
