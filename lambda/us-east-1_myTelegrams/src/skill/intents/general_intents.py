from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.exceptions import respond_to_http_error_code
from src.skill.utils.constants import Constants


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        i18n = Constants.i18n
        speech_text = i18n.HELP

        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        i18n = Constants.i18n
        speech_text = i18n.get_random_goodbye()

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = Constants.i18n
        speech_text = i18n.FALLBACK_INTENT
        reprompt = i18n.FALLBACK_INTENT_REPROMPT

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        sess_attrs.clear()

        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class CatchBackendExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        sess_attrs = handler_input.attributes_manager.session_attributes

        if sess_attrs.get("HTTP_ERROR_CODE"):
            return True

    def handle(self, handler_input, exception):
        sess_attrs = handler_input.attributes_manager.session_attributes

        response = respond_to_http_error_code(handler_input, sess_attrs.get("HTTP_ERROR_CODE"))
        return response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print("Encountered following exception: {}".format(exception))
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = Constants.i18n
        user_account = sess_attrs.get("ACCOUNT", {})

        if not user_account:
            speech = i18n.ACCOUNT_LINKING_REQUIRED
        elif not user_account.get("AUTHORIZED"):
            speech = i18n.NOT_AUTHORIZED_DETOUR
        else:
            # Technically also backend exceptions will be logged here. E.G.: if problem when
            # sending a telegram. I don't catch all Backend exceptions, only on account
            # interceptor
            speech = i18n.FRONTEND_ERROR

        handler_input.response_builder.speak(speech).set_should_end_session(True)

        return handler_input.response_builder.response
