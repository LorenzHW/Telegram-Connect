import unittest

from src.tests.settings_intent.settings_requests import settings_request_1, settings_request_2
from src.tests.secret import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from lambda_function import sb


class AlexaParticleTests(unittest.TestCase):
    def test_settings_intent(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        settings_request_1["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        settings_request_1["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(settings_request_1, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml[7:-8], i18n.SETTINGS_OPENED)

        settings_request_2["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        settings_request_2["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(settings_request_2, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[7:25]
        self.assertTrue(ssml in i18n.NON_VERBOSE_CHOICE.format(
            'enable') or ssml in i18n.NON_VERBOSE_CHOICE.format('disable'))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("test_settings_intent"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
