from ask_sdk_core.dispatch_components import AbstractRequestInterceptor, AbstractResponseInterceptor
from ask_sdk_model.ui import SimpleCard, LinkAccountCard

from src.skill.services.daily_telegrams_service import DailyTelegramsService
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import BackendException
from src.skill.utils.utils import convert_speech_to_text


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


class CardResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        sess_attrs = handler_input.attributes_manager.session_attributes

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

        if not sess_attrs.get("ACCOUNT") and Constants.ACCESS_TOKEN:
            try:
                account = DailyTelegramsService().get_daily_telegrams_account()
                sess_attrs["ACCOUNT"] = {
                    "ID": account.id,
                    "PHONE_NUMBER": account.phone_number,
                    "AUTHORIZED": account.is_authorized
                }
            except BackendException as http_error_code:
                sess_attrs["HTTP_ERROR_CODE"] = http_error_code.args[0]
