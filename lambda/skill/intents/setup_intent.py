from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog import ElicitSlotDirective
from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, PhoneNumberUnoccupied, SessionPasswordNeeded

from skill.i18n.util import get_i18n
from skill.intents.general_intents import CatchAllExceptionHandler
from skill.services.alexa_settings_service import AlexaSettingsService
from skill.state_manager import StateManager
from skill.pyrogram.pyrogram_manager import PyrogramManager


class SetupIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("SetupIntent")(handler_input):
            return True

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(handler_input.request_envelope.request.locale, sess_attrs.get("tz_database_name"))

        slots = handler_input.request_envelope.request.intent.slots
        pyrogram_manager = PyrogramManager(StateManager(handler_input))
        settings_service = AlexaSettingsService(handler_input.request_envelope.context.system,
                                                handler_input.request_envelope.request.locale)

        if pyrogram_manager.is_authorized:
            return handler_input.response_builder.speak(i18n.ALREADY_AUTHORIZED).set_should_end_session(True).response

        code = slots.get('code').value
        if code:
            try:
                pyrogram_manager.sign_in(sess_attrs['phone_num'], sess_attrs['phone_code_hash'], code)
            except PhoneCodeInvalid:
                speech_text = i18n.PHONE_CODE_INVALID.format(code)
                if 'phone_code_invalid' in sess_attrs:
                    speech_text = i18n.PHONE_CODE_INVALID_2.format(code)
                    return handler_input.response_builder.speak(speech_text).response
                self.add_elicit_slot_directive(handler_input)
                return handler_input.response_builder.speak(speech_text).ask(i18n.FALLBACK).response
            except PhoneCodeExpired:
                return handler_input.response_builder.speak(i18n.PHONE_CODE_EXPIRED).response
            except SessionPasswordNeeded:
                return handler_input.response_builder.speak(i18n.TWO_STEP_ON).response
            except Exception:
                return CatchAllExceptionHandler().handle(handler_input, Exception('Exception during Sign In'))
            return handler_input.response_builder.speak(i18n.SUCCESS_SETUP).set_should_end_session(True).response

        phone_num = sess_attrs.get('phone_num')
        if not phone_num:
            phone_num = settings_service.get_phone_number()
            if phone_num == 'ACCESS_DENIED':
                sess_attrs['show_permission_consent_card'] = True
                return handler_input.response_builder.speak(i18n.NO_PERMISSION).set_should_end_session(True).response
            elif phone_num == '':
                return handler_input.response_builder.speak(i18n.NO_PHONE_NUMBER).set_should_end_session(True).response
            sess_attrs['phone_num'] = phone_num

        try:
            phone_code_hash = pyrogram_manager.send_code(phone_num)
        except PhoneNumberUnoccupied:
            return handler_input.response_builder.speak(i18n.PHONE_NUM_UNOCCUPIED).response

        sess_attrs['phone_code_hash'] = phone_code_hash
        self.add_elicit_slot_directive(handler_input)
        return handler_input.response_builder.speak(i18n.CODE_SENT).ask(i18n.FALLBACK).response

    def add_elicit_slot_directive(self, handler_input):
        intent = handler_input.request_envelope.request.intent
        slot_directive = ElicitSlotDirective(slot_to_elicit='code', updated_intent=intent)
        handler_input.response_builder.add_directive(slot_directive)
