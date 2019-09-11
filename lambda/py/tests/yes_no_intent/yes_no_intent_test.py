import unittest

from tests.yes_no_intent.yes_requests import yes_on_listen_to_new_telegrams, send_yes_telegram
from tests.yes_no_intent.no_requests import *
from tests.tokens import VALID_TOKEN
from skill.services.telethon_service import TelethonService
from skill.i18n.language_model import LanguageModel
from skill.utils.constants import Constants
from skill.utils.utils import set_language_model
from skill.lambda_function import sb


class YesNoIntentTest(unittest.TestCase):
    def yes_intent_on_new_telegrams(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        yes_on_listen_to_new_telegrams["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_on_listen_to_new_telegrams["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_on_listen_to_new_telegrams, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-31:-8] in i18n.REPLY_OR_NEXT_TELEGRAM
                        or ssml[-31:-8] in i18n.REPLY_SEND_OR_STOP
                        or ssml[-40:-8] in i18n.NO_TELEGRAMS)

    def yes_on_send_telegram(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        send_yes_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_yes_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_yes_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml.split('.')[1][1:-8]
        self.assertTrue(test_case in i18n.ANYTHING_ELSE)
        


    def no_intent_on_new_telegrams(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # User answered No on question: "Welcome, do you want to hear your new Telegrams?"
        no_on_listen_to_new_telegrams["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        no_on_listen_to_new_telegrams["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(no_on_listen_to_new_telegrams, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[-33:-8]
        self.assertTrue(ssml in i18n.HELP_USER)

    def no_on_send_telegram(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        send_no_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_no_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_no_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml.split('.')[1][1:-8]
        self.assertTrue(test_case in i18n.ANYTHING_ELSE)


if __name__ == "__main__":
    set_language_model('en-US', True)
    Constants.ACCESS_TOKEN = VALID_TOKEN
    suite = unittest.TestSuite()

    suite.addTest(YesNoIntentTest("no_intent_on_new_telegrams"))
    suite.addTest(YesNoIntentTest("yes_intent_on_new_telegrams"))
    suite.addTest(YesNoIntentTest("yes_on_send_telegram"))
    suite.addTest(YesNoIntentTest("no_on_send_telegram"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


