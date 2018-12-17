from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type

from src.ask_sdk_custom.ask_sdk_core_custom.skill_builder_custom import SkillBuilderCustom
from src.ask_sdk_custom.ask_sdk_model_custom.can_fulfill_intent_custom import CanFulfillIntentCustom
from src.ask_sdk_custom.ask_sdk_model_custom.can_fulfill_response_custom import \
    CanFulfillResponseCustom
from src.ask_sdk_custom.ask_sdk_model_custom.can_fulfill_slot_custom import CanFulfillSlotCustom
from src.skill.i18n.language_model import LanguageModel
from src.skill.intents.general_intents import HelpIntentHandler, CancelOrStopIntentHandler, \
    FallbackIntentHandler, SessionEndedRequestHandler, CatchAllExceptionHandler, \
    CatchBackendExceptionHandler
from src.skill.intents.interceptors import LoggingRequestInterceptor, CardResponseInterceptor, \
    PreviousIntentInterceptor, AccountInterceptor
from src.skill.intents.message_intent import MessageIntentHandler
from src.skill.intents.send_intent import SendIntentHandler
from src.skill.intents.speed_intent import SpeedIntentHandler
from src.skill.intents.yes_no_intents import YesIntentHandler, NoIntentHandler
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import TelethonException, handle_telethon_error_response

sb = SkillBuilderCustom()


class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for skill launch

    Arguments:
        AbstractRequestHandler {[type]} -- [description]
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        """
        Three cases:
        1. User did not link account --> provide user with necessary information
        2. User linked account but is not authorized --> ask if he wants to authorize
        3. User linked account and is authorized --> check for new telegrams.

        Arguments:
            handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.

        Returns:
            [ask_sdk_model.response.Response] -- Response object
        """
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
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


class CanFulfillIntentRequestHandler(AbstractRequestHandler):
    """
    For name free interaction with the skill. See:
    https://developer.amazon.com/docs/custom-skills/understand-name-free-interaction-for-custom-skills.html

    Arguments:
        AbstractRequestHandler {[type]} -- [description]
    """
    def can_handle(self, handler_input):
        return is_request_type("CanFulfillIntentRequest")(handler_input)

    def handle(self, handler_input):
        name = handler_input.request_envelope.request.intent.get("name")

        if name == "SendIntent":
            can_fulfill_first_name_slot = CanFulfillSlotCustom("YES")
            can_fulfill_message_slot = CanFulfillSlotCustom()

            slots = {"first_name": can_fulfill_first_name_slot, "message": can_fulfill_message_slot}
            can_fulfill_intent = CanFulfillIntentCustom("MAYBE", slots)
            response = CanFulfillResponseCustom(can_fulfill_intent)
        elif name == "MessageIntent":
            can_fulfill_intent = CanFulfillIntentCustom("MAYBE")
            response = CanFulfillResponseCustom(can_fulfill_intent)
        elif name == "CustomYesIntent":
            can_fulfill_message_slot = CanFulfillSlotCustom()
            can_fulfill_code_slot = CanFulfillSlotCustom()

            slots = {"message": can_fulfill_message_slot, "code": can_fulfill_code_slot}
            can_fulfill_intent = CanFulfillIntentCustom("NO", slots)
            response = CanFulfillResponseCustom(can_fulfill_intent)
        elif name == "SpeedIntent":
            can_fulfill_speed_dial_number_slot = CanFulfillSlotCustom("YES")
            can_fulfill_message_slot = CanFulfillSlotCustom()

            slots = {"speed_dial_number": can_fulfill_speed_dial_number_slot,
                     "message": can_fulfill_message_slot}
            can_fulfill_intent = CanFulfillIntentCustom("MAYBE", slots)
            response = CanFulfillResponseCustom(can_fulfill_intent)
        else:
            can_fulfill_intent = CanFulfillIntentCustom("NO")
            response = CanFulfillResponseCustom(can_fulfill_intent)

        return response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CanFulfillIntentRequestHandler())
sb.add_request_handler(SendIntentHandler())
sb.add_request_handler(SpeedIntentHandler())
sb.add_request_handler(MessageIntentHandler())
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

handler = sb.lambda_handler()
