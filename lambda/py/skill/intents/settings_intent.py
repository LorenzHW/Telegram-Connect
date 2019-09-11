from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog import ElicitSlotDirective, DelegateDirective
from ask_sdk_model import Intent

from skill.i18n.language_model import LanguageModel
from skill.services.daily_telegrams_service import DailyTelegramsService
from skill.models.general_models import Settings
from skill.utils.utils import set_language_model
from skill.utils.constants import Constants
from ask_sdk_model.slu.entityresolution import StatusCode


class SettingsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        user_is_authorized = sess_attrs.get("ACCOUNT", {}).get("AUTHORIZED")
        return is_intent_name("SettingsIntent")(handler_input) and user_is_authorized

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = Constants.i18n
        current_intent = handler_input.request_envelope.request.intent
        settings_id = sess_attrs.get('ACCOUNT').get('SETTINGS_ID')
        daily_telegram_service = DailyTelegramsService()

        if settings_id is None:
            settings_id = daily_telegram_service.create_settings()
            sess_attrs['ACCOUNT']['SETTINGS_ID'] = settings_id

        for slot_name, current_slot in current_intent.slots.items():
            if slot_name == 'enable_or_disable_non_verbose_mode':
                if current_slot.value is None:
                    speech_text = i18n.SETTINGS_OPENED
                    slot_to_elicit = 'enable_or_disable_non_verbose_mode'
                    elicit_directive = ElicitSlotDirective(
                        current_intent, slot_to_elicit)
                    handler_input.response_builder.add_directive(
                        elicit_directive)
                else:
                    # If another configuration will be added I have to move the logic here
                    if current_slot.resolutions.resolutions_per_authority[0].status.code == StatusCode.ER_SUCCESS_MATCH:
                        val = current_slot.resolutions.resolutions_per_authority[0].values[0].value
                        if val.name.lower() in ['enable', 'einschalten']:
                            non_verbose_mode = True
                            speech_text = i18n.NON_VERBOSE_CHOICE.format(
                                i18n.ENABLE)
                        else:
                            non_verbose_mode = False
                            speech_text = i18n.NON_VERBOSE_CHOICE.format(
                                i18n.DISABLE)

                        settings = Settings(settings_id, non_verbose_mode)
                        settings = daily_telegram_service.update_settings(settings)

                        locale = handler_input.request_envelope.request.locale
                        set_language_model(locale, settings.non_verbose_mode)
                    else:
                        # User did not say 'enable' or 'disable'
                        non_verbose_mode = False
                        speech_text = i18n.HINT_DISABLE_ENABLE

                    speech_text += ' ' + i18n.LEAVING_SETTINGS_MODE
                    speech_text += ' ' + i18n.get_random_anyting_else_without_ack()

        handler_input.response_builder \
            .speak(speech_text).set_should_end_session(False).ask(i18n.FALLBACK)
        return handler_input.response_builder.response
