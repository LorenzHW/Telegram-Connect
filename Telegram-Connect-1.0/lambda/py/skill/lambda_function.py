from ask_sdk.standard import StandardSkillBuilder

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from skill.i18n.language_model import LanguageModel
from skill.intents.general_intents import HelpIntentHandler, CancelOrStopIntentHandler, \
    FallbackIntentHandler, SessionEndedRequestHandler, CatchAllExceptionHandler, \
    CatchBackendExceptionHandler
from skill.intents.interceptors import LoggingRequestInterceptor, CardResponseInterceptor, \
    PreviousIntentInterceptor, AccountInterceptor
from skill.intents.message_intent import MessageIntentHandler
from skill.intents.reply_intent import ReplyIntentHandler
from skill.intents.settings_intent import SettingsIntentHandler
from skill.intents.authorization_intent import AuthorizationIntentHandler
from skill.intents.send_intent import SendIntentHandler
from skill.intents.speed_intent import SpeedIntentHandler
from skill.intents.yes_no_intents import YesIntentHandler, NoIntentHandler
from skill.services.telethon_service import TelethonService
from skill.utils.constants import Constants
from skill.utils.exceptions import TelethonException, handle_telethon_error_response

sb = StandardSkillBuilder()


class LaunchRequestHandler(AbstractRequestHandler):
    # Handler for Skill Launch
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        i18n = Constants.i18n
        sess_attrs = handler_input.attributes_manager.session_attributes

        if not Constants.ACCESS_TOKEN:
            speech_text = i18n.ACCOUNT_LINKING_REQUIRED
            handler_input.response_builder.speak(speech_text).set_should_end_session(True)
            sess_attrs["LINK_ACCOUNT_CARD"] = True
            return handler_input.response_builder.response

        user_is_authorized = sess_attrs.get("ACCOUNT").get("AUTHORIZED")
        telethon_service = TelethonService()

        if user_is_authorized:
            try:
                user_has_telegrams = telethon_service.check_telegrams()
            except TelethonException as error:
                return handle_telethon_error_response(error, handler_input)

            if user_has_telegrams:
                speech_text = i18n.USER_HAS_TELEGRAMS
            else:
                speech_text = i18n.WELCOME
        else:
            speech_text = i18n.NOT_AUTHORIZED

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(i18n.FALLBACK)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SendIntentHandler())
sb.add_request_handler(SpeedIntentHandler())
sb.add_request_handler(MessageIntentHandler())
sb.add_request_handler(ReplyIntentHandler())
sb.add_request_handler(SettingsIntentHandler())
sb.add_request_handler(AuthorizationIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_request_interceptor(AccountInterceptor())
sb.add_global_response_interceptor(CardResponseInterceptor())
sb.add_global_response_interceptor(PreviousIntentInterceptor())

sb.add_exception_handler(CatchBackendExceptionHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
