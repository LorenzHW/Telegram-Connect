import unittest

from src.tests.reply_intent.reply_requests import reply_request
from src.tests.tokens import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants
from lambda_function import sb



class AlexaParticleTests(unittest.TestCase):
    
    def reply(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        reply_request["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        reply_request["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(reply_request, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-29:-8] in i18n.MESSAGE_2)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    Constants.ACCESS_TOKEN = VALID_TOKEN
    suite.addTest(AlexaParticleTests("reply"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
