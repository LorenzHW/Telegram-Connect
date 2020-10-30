import traceback

from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from skill.i18n.util import get_i18n


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(handler_input.request_envelope.request.locale, sess_attrs.get("tz_database_name"))
        return handler_input.response_builder.speak(i18n.HELP).ask(i18n.FALLBACK).response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):  # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(handler_input.request_envelope.request.locale, sess_attrs.get("tz_database_name"))
        return handler_input.response_builder.speak(i18n.SUGGEST_WHAT_TO_DO).ask(i18n.FALLBACK).response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        locale = handler_input.request_envelope.request.locale
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(locale, sess_attrs.get("tz_database_name"))

        speech_text = " " + i18n.get_random_goodbye()
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Triggered {}.".format(intent_name)
        return handler_input.response_builder.speak(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        print("ENCOUNTERED FOLLOWING EXCEPTION:")
        print("PRINTING: TRACEBACK: ")
        print(traceback.format_exc())
        print(exception)
        rb = handler_input.response_builder
        locale = handler_input.request_envelope.request.locale
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(locale, sess_attrs.get("tz_database_name", "America/Los_Angeles"))

        sess_attrs = handler_input.attributes_manager.session_attributes
        sess_attrs.clear()

        speech = i18n.EXCEPTION

        rb.speak(speech).set_should_end_session(True)
        return rb.response
