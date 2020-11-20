import pytz

from skill.i18n.language_model_de import LanguageModelDE
from skill.i18n.language_model_en import LanguageModelEN


def update_request(request, locale):
    request["session"]["user"]["userId"] = "NOT_RELEVANT_AND_THERE_SHOULDNT_BE_A_DYNAMO_DB_ENTRY"
    request["context"]["System"]["user"]["userId"] = "NOT_RELEVANT_AND_THERE_SHOULDNT_BE_A_DYNAMO_DB_ENTRY"
    request["request"]["locale"] = locale
    return request


def get_i18n_for_tests(locale):
    timezone = pytz.timezone("America/Los_Angeles")
    language_model = LanguageModelEN(timezone)
    if locale == 'de-DE':
        language_model = LanguageModelDE(timezone)
    return language_model
