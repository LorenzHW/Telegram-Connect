from typing import Union

import pytz
from ask_sdk_core.handler_input import HandlerInput

from skill.i18n.language_model_de import LanguageModelDE
from skill.i18n.language_model_en import LanguageModelEN


def get_i18n(handler_input: HandlerInput) -> Union[LanguageModelEN, LanguageModelDE]:
    tz_database_name = handler_input.attributes_manager.session_attributes.get("tz_database_name",
                                                                               "America/Los_Angeles")
    timezone = pytz.timezone(tz_database_name)
    language_model = LanguageModelEN(timezone)
    locale = handler_input.request_envelope.request.locale
    if locale == 'de-DE':
        language_model = LanguageModelDE(timezone)
    return language_model
