
import unittest

from src.tests.authorization_intent.authorization_requests import no_phone_added
from src.tests.tokens import VALID_TOKEN
from src.skill.i18n.non_verbose_language_model import NonVerboseLanguageModel
from lambda_function import sb


class AlexaParticleTests(unittest.TestCase):
    def authorization_with_no_phone(self):
        i18n = NonVerboseLanguageModel('de-DE', False)
        handler = sb.lambda_handler()

        # User wants to authorize: user did not add phone number
        no_phone_added["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        no_phone_added["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(no_phone_added, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.NO_PHONE))

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("authorization_with_no_phone"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
