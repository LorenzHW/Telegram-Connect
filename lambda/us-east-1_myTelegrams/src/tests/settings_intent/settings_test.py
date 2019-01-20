import unittest

from src.tests.settings_intent.settings_requests import open_settings_first_time, enable_non_verbose_mode, open_settings
from src.tests.tokens import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants
from lambda_function import sb


class AlexaParticleTests(unittest.TestCase):
    def test_settings_intent(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # "In settings mode. Do you want to enable or disable non-verbose mode?"
        open_settings["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        open_settings["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(open_settings, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml[7:-8], i18n.SETTINGS_OPENED)
        
        # "Non verbose mode enabled / disabled"
        enable_non_verbose_mode["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        enable_non_verbose_mode["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(enable_non_verbose_mode, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[7:25]
        self.assertTrue(ssml in i18n.NON_VERBOSE_CHOICE.format(
            'enable') or ssml in i18n.NON_VERBOSE_CHOICE.format('disable'))

        

    def test_first_time_setting_intent(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # Creates a new settings object in backend
        open_settings_first_time["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        open_settings_first_time["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(open_settings_first_time, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml[7:-8], i18n.SETTINGS_OPENED)



if __name__ == "__main__":
    suite = unittest.TestSuite()
    Constants.ACCESS_TOKEN = VALID_TOKEN
    suite.addTest(AlexaParticleTests("test_settings_intent"))
    # suite.addTest(AlexaParticleTests("test_first_time_setting_intent"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
