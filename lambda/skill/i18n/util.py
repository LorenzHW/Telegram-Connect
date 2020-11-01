from typing import Union

import pytz

from skill.i18n.language_model_en import LanguageModelEN


def get_i18n(locale: str, tz_database_name: str) -> Union[LanguageModelEN]:
    timezone = pytz.timezone(tz_database_name)

    language_model = LanguageModelEN(timezone)
    if locale == 'de-DE':
        pass
    return language_model
