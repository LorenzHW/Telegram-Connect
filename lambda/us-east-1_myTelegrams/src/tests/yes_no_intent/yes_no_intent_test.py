import unittest

from src.tests.yes_no_intent.yes_requests import *
from src.tests.yes_no_intent.no_requests import *
from src.tests.tokens import VALID_TOKEN
from src.skill.services.telethon_service import TelethonService
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants
from src.skill.utils.utils import set_language_model
from lambda_function import sb



class AlexaParticleTests(unittest.TestCase):
    def yes_intent_on_new_telegrams(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        yes_on_listen_to_new_telegrams["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_on_listen_to_new_telegrams["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_on_listen_to_new_telegrams, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-31:-8] in i18n.REPLY)

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


if __name__ == "__main__":
    set_language_model('en-US', True)
    Constants.ACCESS_TOKEN = VALID_TOKEN
    
    suite = unittest.TestSuite()
    telethon_service = TelethonService()
    got_unread_telegrams = telethon_service.check_telegrams()

    if got_unread_telegrams:
        suite.addTest(AlexaParticleTests("no_intent_on_new_telegrams"))
        suite.addTest(AlexaParticleTests("yes_intent_on_new_telegrams"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)

# TODO: Add yes test on: "Is there anything else I can help you with?
# TODO: Add no test on: "Is there anything else I can help you with?"