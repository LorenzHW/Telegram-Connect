from ask_sdk_core.dispatch_components import AbstractRequestInterceptor, AbstractResponseInterceptor
from ask_sdk_model.ui import SimpleCard

from src.skill.utils.constants import Constants
from src.skill.utils.parser import convert_speech_to_text


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


class CardResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        pass
        response.card = SimpleCard(
            title=Constants.SKILL_NAME,
            content=convert_speech_to_text(response.output_speech.ssml)
        )
