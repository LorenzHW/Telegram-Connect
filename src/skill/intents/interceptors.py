from ask_sdk_core.dispatch_components import AbstractRequestInterceptor, AbstractResponseInterceptor
from ask_sdk_model.ui import SimpleCard

from src.skill.utils.constants import Constants
from src.skill.utils.utils import convert_speech_to_text


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


class CardResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
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
