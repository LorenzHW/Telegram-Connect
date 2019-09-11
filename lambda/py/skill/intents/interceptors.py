from ask_sdk_core.dispatch_components import AbstractRequestInterceptor, AbstractResponseInterceptor
from ask_sdk_model.ui import SimpleCard, LinkAccountCard

from skill.services.daily_telegrams_service import DailyTelegramsService
from skill.utils.constants import Constants
from skill.utils.exceptions import BackendException
from skill.utils.utils import convert_speech_to_text, set_language_model
from skill.i18n.language_model import LanguageModel


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


class CardResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        if handler_input.request_envelope.request.object_type != "CanFulfillIntentRequest":
            sess_attrs = handler_input.attributes_manager.session_attributes
            print(sess_attrs)

            if sess_attrs.get("LINK_ACCOUNT_CARD"):
                response.card = LinkAccountCard()
            else:
                response.card = SimpleCard(
                    title=Constants.SKILL_NAME,
                    content=convert_speech_to_text(response.output_speech.ssml)
                )


class PreviousIntentInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        sess_attrs = handler_input.attributes_manager.session_attributes

        if handler_input.request_envelope.request.object_type == "LaunchRequest":
            sess_attrs["PREV_INTENT"] = "LaunchIntent"
        elif handler_input.request_envelope.request.object_type == "IntentRequest":
            sess_attrs["PREV_INTENT"] = handler_input.request_envelope.request.intent.name


class AccountInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        Constants.ACCESS_TOKEN = handler_input.request_envelope.session.user.access_token
        locale = handler_input.request_envelope.request.locale

        if Constants.i18n is None or handler_input.request_envelope.session.new:
            set_language_model(locale, non_verbose_mode=False)

        

        if not sess_attrs.get("ACCOUNT") and Constants.ACCESS_TOKEN:
            service = DailyTelegramsService()

            try:
                account = service.get_daily_telegrams_account()
                sess_attrs["ACCOUNT"] = {
                    "ID": account.id,
                    "PHONE_NUMBER": account.phone_number,
                    "AUTHORIZED": account.is_authorized,
                    "SETTINGS_ID": account.settings_id
                }

                if account.settings_id:
                    settings = service.get_settings(account.settings_id)
                    set_language_model(locale, settings.non_verbose_mode)
                
            except BackendException as http_error_code:
                sess_attrs["HTTP_ERROR_CODE"] = http_error_code.args[0]
