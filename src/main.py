from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.ui import SimpleCard

from src.skill.i18n.language_model import LanguageModel
from src.skill.intents.general_intents import HelpIntentHandler, CancelOrStopIntentHandler, \
    FallbackIntentHandler, SessionEndedRequestHandler, CatchAllExceptionHandler
from src.skill.intents.interceptors import LoggingRequestInterceptor, CardResponseInterceptor
from src.skill.intents.send_intent import SendIntentHandler

sb = SkillBuilder()


class AbstractDailyTelegramsRequestHandler(AbstractRequestHandler):

    def __init__(self):
        self.i18n = LanguageModel()

    def can_handle(self, handler_input):
        pass

    def handle(self, handler_input):
        pass


class LaunchRequestHandler(AbstractRequestHandler):
    # Handler for Skill Launch
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        i18n = LanguageModel(handler_input.request_envelope.request.locale)

        speech_text = i18n.WELCOME

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SendIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(CardResponseInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
