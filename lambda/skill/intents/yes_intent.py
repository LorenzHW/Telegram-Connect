from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent, Slot
from ask_sdk_model.dialog import DelegateDirective

from skill.helper_functions import ExploreIntents
from skill.i18n.util import get_i18n


class YesIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("AMAZON.YesIntent")(handler_input):
            return True

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        intent_to_explore = sess_attrs.get("explore_intent", "")
        i18n = get_i18n(handler_input.request_envelope.request.locale, sess_attrs.get("tz_database_name"))

        if intent_to_explore == ExploreIntents.EXPLORE_SETUP_INTENT:
            slots = {"code": Slot(name="code")}
            intent = Intent(name='SetupIntent', slots=slots)
            handler_input.response_builder.add_directive(DelegateDirective(updated_intent=intent))
            return handler_input.response_builder.response

        if intent_to_explore == ExploreIntents.EXPLORE_MESSAGE_INTENT:
            intent = Intent(name='MessageIntent')
            handler_input.response_builder.add_directive(DelegateDirective(updated_intent=intent))
            return handler_input.response_builder.response

        return handler_input.response_builder.speak(i18n.SUGGEST_WHAT_TO_DO).ask(i18n.FALLBACK).response
