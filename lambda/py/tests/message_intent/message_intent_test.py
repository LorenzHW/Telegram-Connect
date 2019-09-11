import unittest

from tests.message_intent.message_requests import new_telegrams, multiple_messages_last_one
from tests.tokens import VALID_TOKEN
from skill.i18n.language_model import LanguageModel
from skill.utils.constants import Constants
from skill.utils.utils import set_language_model
from skill.services.telethon_service import TelethonService
from skill.lambda_function import sb


class MessageIntentTest(unittest.TestCase):
    def test_open_message_intent(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # User: "Check my telegrams".
        new_telegrams["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        new_telegrams["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(new_telegrams, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-31:-8] in i18n.REPLY_OR_NEXT_TELEGRAM
                        or ssml[-31:-8] in i18n.REPLY_SEND_OR_STOP
                        or ssml[-40:-8] in i18n.NO_TELEGRAMS)

    def test_multiple_telegrams(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # User: "Next telegram" (last one)
        multiple_messages_last_one["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        multiple_messages_last_one["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(multiple_messages_last_one, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-31:-8] in i18n.REPLY_SEND_OR_STOP)


if __name__ == "__main__":
    set_language_model('en-US', True)
    Constants.ACCESS_TOKEN = VALID_TOKEN

    suite = unittest.TestSuite()
    suite.addTest(MessageIntentTest("test_open_message_intent"))
    suite.addTest(MessageIntentTest("test_multiple_telegrams"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
