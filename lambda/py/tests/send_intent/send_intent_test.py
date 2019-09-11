import unittest

from tests.send_intent.send_requests import *
from tests.tokens import VALID_TOKEN
from skill.i18n.language_model import LanguageModel
from skill.utils.constants import Constants
from skill.utils.utils import set_language_model
from skill.lambda_function import sb


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

        # U: 'Lorenz'
        # Alexa now asks for message
        ask_for_message["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        ask_for_message["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(ask_for_message, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[19:-8] in i18n.MESSAGE.format('Lorenz'))

    def send_telegram(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        send_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml.split('.')[1][1:-8]
        self.assertTrue(test_case in i18n.ANYTHING_ELSE)

    def test_multiple_choices(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # A: "First name"
        # U: "Mik"
        multiple_choices["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        multiple_choices["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(multiple_choices, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[7:15] in i18n.NO_CONTACT)

        # A: "I found: 1 Michael, 2 Martin, and 3 Riki."
        # U: "One"
        user_made_choice["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        user_made_choice["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(user_made_choice, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-17:-8] in i18n.MESSAGE.format('Michael'))

        # A: "I found: 1 Michael, 2 Martin, and 3 Riki."
        # U: "Mik"
        user_says_wrong_on_choice["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        user_says_wrong_on_choice["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(user_says_wrong_on_choice, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[7:30] in i18n.MAX_NO_CONTACT)

    def test_send_intent_with_speed_number(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # U: "10"
        # Alexa asks for message
        ask_for_message_speed_dial["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        ask_for_message_speed_dial["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(ask_for_message_speed_dial, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[19:-8] in i18n.MESSAGE.format('Lorenz'))

        # U: "111"
        # Alexa: "No speed dial contact"
        ask_for_message_speed_dial["request"]["intent"]["slots"]["first_name"]["value"] = "111"
        event = handler(ask_for_message_speed_dial, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[19:-8] in i18n.NO_SPEED_DIAL_CONTACT)

    def german_speed_dial(self):
        set_language_model('de-DE', True)
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        german_speed_dial["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        german_speed_dial["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(german_speed_dial, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[19:-8] in i18n.MESSAGE.format('Lorenz'))

        set_language_model('en-US', True)

if __name__ == "__main__":
    set_language_model('en-US', True)

    suite = unittest.TestSuite()
    suite.addTest(SendIntentTest("start_send_intent"))
    suite.addTest(SendIntentTest("ask_for_message"))
    suite.addTest(SendIntentTest("send_telegram"))
    suite.addTest(SendIntentTest("test_multiple_choices"))
    suite.addTest(SendIntentTest("test_send_intent_with_speed_number"))
    suite.addTest(SendIntentTest("german_speed_dial"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
