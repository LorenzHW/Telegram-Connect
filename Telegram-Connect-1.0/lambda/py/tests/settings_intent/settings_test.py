import unittest

from tests.settings_intent.settings_requests import open_settings_first_time, enable_non_verbose_mode, open_settings
from tests.tokens import VALID_TOKEN
from skill.i18n.language_model import LanguageModel
from skill.utils.constants import Constants
from skill.utils.utils import set_language_model
from skill.services.daily_telegrams_service import DailyTelegramsService
from skill.lambda_function import sb


class SettingsIntentTest(unittest.TestCase):
    def test_settings_intent(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()
        service = DailyTelegramsService()
        account = service.get_daily_telegrams_account()

        # User: "Open settings"
        open_settings["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        open_settings["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(open_settings, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml[7:-8], i18n.SETTINGS_OPENED)

        # A: "In settings mode. Do you want to enable or disable non-verbose mode?"
        # U: "Enable/disable non-verbose mode"
        enable_non_verbose_mode["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        enable_non_verbose_mode["session"]["user"]["accessToken"] = VALID_TOKEN
        enable_non_verbose_mode["session"]["attributes"]["ACCOUNT"]["SETTINGS_ID"] = account.settings_id
        event = handler(enable_non_verbose_mode, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[7:25]
        self.assertTrue(ssml in i18n.NON_VERBOSE_CHOICE.format(
            'enable') or ssml in i18n.NON_VERBOSE_CHOICE.format('disable'))

    def test_first_time_setting_intent(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # Creates a new settings object in backend
        open_settings_first_time["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        open_settings_first_time["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(open_settings_first_time, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml[7:-8], i18n.SETTINGS_OPENED)


if __name__ == "__main__":
    set_language_model('en-US', True)
    Constants.ACCESS_TOKEN = VALID_TOKEN

    suite = unittest.TestSuite()
    suite.addTest(SettingsIntentTest("test_first_time_setting_intent"))
    suite.addTest(SettingsIntentTest("test_settings_intent"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
