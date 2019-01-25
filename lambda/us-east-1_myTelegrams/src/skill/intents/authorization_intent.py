from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog import ElicitSlotDirective, DelegateDirective
from ask_sdk_model import Intent

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.exceptions import TelethonException, handle_telethon_error_response
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants


class AuthorizationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AuthorizationIntent")(handler_input)

    def handle(self, handler_input):
        i18n = Constants.i18n
        telethon_service = TelethonService()
        sess_attrs = handler_input.attributes_manager.session_attributes
        user_is_authorized = sess_attrs.get("ACCOUNT").get("AUTHORIZED")
        account = sess_attrs.get("ACCOUNT")
        slots = handler_input.request_envelope.request.intent.slots
        reprompt = None

        if user_is_authorized:
            speech_text = i18n.ALREADY_AUTHORIZED
            handler_input.response_builder.speak(speech_text) \
                .set_should_end_session(False).ask(i18n.FALLBACK)
            return handler_input.response_builder.response
        if not account.get("PHONE_NUMBER"):
            speech_text = i18n.NO_PHONE
            should_end = True
        elif not slots.get("code").value:
            try:
                phone_code_hash = telethon_service.send_code_request()
            except TelethonException as error:
                return handle_telethon_error_response(error, handler_input).response_builder.response

            sess_attrs["PHONE_CODE_HASH"] = phone_code_hash

            updated_intent = Intent("AuthorizationIntent", slots)
            elicit_directive = ElicitSlotDirective(updated_intent, "code")
            handler_input.response_builder.add_directive(elicit_directive)

            speech_text = i18n.WHAT_IS_CODE
            reprompt = i18n.WHAT_IS_CODE_REPROMPT
            should_end = False
        else:
            phone_code_hash = sess_attrs.get("PHONE_CODE_HASH")
            try:
                ok = telethon_service.sign_user_in(
                    slots.get("code").value, phone_code_hash)
            except TelethonException as error:
                return handle_telethon_error_response(error, handler_input).response_builder.response

            if ok:
                sess_attrs["ACCOUNT"]["AUTHORIZED"] = True
                speech_text = i18n.AUTHORIZED
                reprompt = i18n.FALLBACK
                should_end = False
            else:
                speech_text = i18n.WRONG_CODE
                should_end = True

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(should_end)
        if reprompt:
            handler_input.response_builder.ask(reprompt)

        return handler_input.response_builder.response
