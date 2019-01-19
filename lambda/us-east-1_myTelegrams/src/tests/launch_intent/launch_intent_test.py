import unittest

from lambda_function import sb
from src.tests.launch_intent.launch_request import launch_request
from src.skill.i18n.language_model import LanguageModel
from src.tests.secret import *

class AlexaParticleTests(unittest.TestCase):
    def test_authorized_launch_request(self):
        i18n = LanguageModel('en-US')
        launch_request_copy = launch_request
        handler = sb.lambda_handler()

        launch_request_copy["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        launch_request_copy["session"]["user"]["accessToken"] = VALID_TOKEN

        event = handler(launch_request_copy, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml == '<speak>{}</speak>'.format(i18n.WELCOME) or ssml == '<speak>{}</speak>'.format(i18n.USER_HAS_TELEGRAMS))


    def test_account_not_linked_launch_request(self):
        i18n = LanguageModel('en-US')
        launch_request_copy = launch_request
        handler = sb.lambda_handler()
        
        # Remove access token to simulate a user who did not link account
        launch_request_copy["context"]["System"]["user"]["accessToken"] = None
        launch_request_copy["session"]["user"]["accessToken"] = None
        
        event = handler(launch_request_copy, None)
        ssml = ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.ACCOUNT_LINKING_REQUIRED))

    def test_account_not_authorized_launch_request(self):
        i18n = LanguageModel('en-US')
        launch_request_copy = launch_request
        handler = sb.lambda_handler()
        
        launch_request_copy["context"]["System"]["user"]["accessToken"] = ALWAYS_VALID_NOT_AUTHORIZED_TOKEN
        launch_request_copy["session"]["user"]["accessToken"] = ALWAYS_VALID_NOT_AUTHORIZED_TOKEN
        
        event = handler(launch_request_copy, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.NOT_AUTHORIZED))

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("test_authorized_launch_request"))
    suite.addTest(AlexaParticleTests("test_account_not_linked_launch_request"))
    suite.addTest(AlexaParticleTests("test_account_not_authorized_launch_request"))
    runner = unittest.TextTestRunner()
    runner.run(suite)