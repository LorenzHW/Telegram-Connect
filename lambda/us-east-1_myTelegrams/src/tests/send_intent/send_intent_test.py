import unittest

from src.tests.send_intent.send_requests import *
from src.tests.tokens import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants
from src.skill.utils.utils import set_language_model
from lambda_function import sb


class SendIntentTest(unittest.TestCase):

    def start_send_intent(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # User says: "Send a telegram"
        start_send_intent["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        start_send_intent["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(start_send_intent, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-16:-8] in i18n.FIRST_NAME)

    def ask_for_message(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # User answered with a first name of the contact
        ask_for_message["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        ask_for_message["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(ask_for_message, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(
            ssml, '<speak>{}</speak>'.format(i18n.MESSAGE.format('Lorenz')))

    def send_telegram(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        send_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml.split('.')[1][1:-8]
        self.assertTrue(test_case in i18n.ANYTHING_ELSE)


if __name__ == "__main__":
    set_language_model('en-US', True)

    suite = unittest.TestSuite()
    suite.addTest(SendIntentTest("start_send_intent"))
    suite.addTest(SendIntentTest("ask_for_message"))
    suite.addTest(SendIntentTest("send_telegram"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    
