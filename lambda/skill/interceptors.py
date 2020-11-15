import pytz
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor, AbstractResponseInterceptor
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard, AskForPermissionsConsentCard

from skill.helper_functions import remove_ssml_tags
from skill.i18n.util import get_i18n
from skill.services.alexa_settings_service import AlexaSettingsService
from skill.state_manager import StateManager


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


class CardResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(handler_input)

        if response.output_speech:
            response.card = SimpleCard(
                title=i18n.SKILL_NAME,
                content=remove_ssml_tags(response.output_speech.ssml)
            )

        if sess_attrs.get('show_permission_consent_card', False):
            sess_attrs['show_permission_consent_card'] = False
            response.card = AskForPermissionsConsentCard(
                ['alexa::profile:mobile_number:read']
            )


class StateRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input: HandlerInput) -> None:
        if handler_input.request_envelope.session.new:
            sess_attrs = handler_input.attributes_manager.session_attributes
            settings_service = AlexaSettingsService(handler_input.request_envelope.context.system,
                                                    handler_input.request_envelope.request.locale)
            tz_database_name = settings_service.get_tz_database_name()
            sess_attrs["tz_database_name"] = tz_database_name
            state_manager = StateManager(handler_input)

            state_manager.state.new_session_count += 1

            handler_input.attributes_manager.persistent_attributes = state_manager.state.to_dict()
            handler_input.attributes_manager.save_persistent_attributes()
