from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.dialog import ElicitSlotDirective
from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, PhoneNumberUnoccupied, SessionPasswordNeeded

from skill.exceptions.all_exceptions import CatchNoSuccessRetrievingPhonenumberExceptionHandler, \
    NoSuccessRetrievingPhonenumberException, CatchAllExceptionHandler
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.services.alexa_settings_service import AlexaSettingsService
from skill.state_manager import StateManager


class SetupIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("SetupIntent")(handler_input):
            return True

    def handle(self, handler_input) -> Response:
        self.sess_attrs = handler_input.attributes_manager.session_attributes
        self.i18n = get_i18n(handler_input)
        self.pyrogram_manager = PyrogramManager(StateManager(handler_input))
        self.handler_input = handler_input

        if self.pyrogram_manager.get_is_authorized():
            return handler_input.response_builder.speak(self.i18n.ALREADY_AUTHORIZED) \
                .set_should_end_session(True).response

        slots = handler_input.request_envelope.request.intent.slots
        code = slots.get('code').value
        if code:
            return self.try_to_sign_user_in(code)
        return self.send_code()

    def add_elicit_slot_directive(self, handler_input):
        intent = handler_input.request_envelope.request.intent
        slot_directive = ElicitSlotDirective(slot_to_elicit='code', updated_intent=intent)
        handler_input.response_builder.add_directive(slot_directive)

    def try_to_sign_user_in(self, code) -> Response:
        try:
            self.pyrogram_manager.sign_in(self.sess_attrs['phone_num'], self.sess_attrs['phone_code_hash'], code)
        except PhoneCodeInvalid:
            speech_text = self.i18n.PHONE_CODE_INVALID.format(code)
            if 'phone_code_invalid' in self.sess_attrs:
                speech_text = self.i18n.PHONE_CODE_INVALID_2.format(code)
                return self.handler_input.response_builder.speak(speech_text).response
            self.add_elicit_slot_directive(self.handler_input)
            return self.handler_input.response_builder.speak(speech_text).ask(self.i18n.FALLBACK).response
        except PhoneCodeExpired:
            return self.handler_input.response_builder.speak(self.i18n.PHONE_CODE_EXPIRED).response
        except SessionPasswordNeeded:
            return self.handler_input.response_builder.speak(self.i18n.TWO_STEP_ON).response
        except Exception:
            return CatchAllExceptionHandler().handle(self.handler_input, Exception('Exception during Sign In'))
        return self.handler_input.response_builder.speak(self.i18n.SUCCESS_SETUP).set_should_end_session(True).response

    def send_code(self) -> Response:
        settings_service = AlexaSettingsService(self.handler_input.request_envelope.context.system,
                                                self.handler_input.request_envelope.request.locale)
        phone_num = self.sess_attrs.get('phone_num')
        if not phone_num:
            phone_num, success = settings_service.get_phone_number()
            if not success and phone_num == 'ACCESS_DENIED':
                self.sess_attrs['show_permission_consent_card'] = True
                return self.handler_input.response_builder.speak(self.i18n.NO_PERMISSION) \
                    .set_should_end_session(True).response
            elif not success:
                return CatchNoSuccessRetrievingPhonenumberExceptionHandler() \
                    .handle(self.handler_input, NoSuccessRetrievingPhonenumberException(phone_num))
            self.sess_attrs["phone_num"] = phone_num

        try:
            phone_code_hash = self.pyrogram_manager.send_code(phone_num)
        except PhoneNumberUnoccupied:
            return self.handler_input.response_builder.speak(self.i18n.PHONE_NUM_UNOCCUPIED).response

        self.sess_attrs['phone_code_hash'] = phone_code_hash
        self.add_elicit_slot_directive(self.handler_input)
        return self.handler_input.response_builder.speak(self.i18n.CODE_SENT).ask(self.i18n.FALLBACK).response
