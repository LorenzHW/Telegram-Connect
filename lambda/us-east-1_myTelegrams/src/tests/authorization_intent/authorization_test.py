
import unittest

from src.tests.authorization_intent.authorization_requests import authorization_request_1, authorization_request_2, authorization_request_3
from src.tests.secret import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from lambda_function import sb


class AlexaParticleTests(unittest.TestCase):
    def authorization_with_no_phone(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # User wants to authorize: user did not add phone number
        authorization_request_1["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        authorization_request_1["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(authorization_request_1, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.NO_PHONE))

    def send_code(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # User wants to authorize: either user receives code
        # This breaks a lot, because we also send request into backend..
        authorization_request_2["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        authorization_request_2["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(authorization_request_2, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml in '<speak>{}</speak>'.format(i18n.WHAT_IS_CODE) or  ssml[:58] in '<speak>{}</speak>'.format(i18n.FLOODWAIT_ERROR))

    def sign_in(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()
        # Set manually
        code = None
        wrong_code = '17832'
        authorization_request_3["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        authorization_request_3["session"]["user"]["accessToken"] = VALID_TOKEN
        
        if code:
            authorization_request_3["request"]["intent"]["slots"]["code"]["value"] = code
            event = handler(authorization_request_3, None)
            ssml = event.get('response').get('outputSpeech').get('ssml')
            ssml = ssml[-127:]
            self.assertTrue(ssml in i18n.AUTHORIZED)
        elif wrong_code:
            authorization_request_3["request"]["intent"]["slots"]["code"]["value"] = wrong_code
            event = handler(authorization_request_3, None)
            ssml = event.get('response').get('outputSpeech').get('ssml')
            ssml = ssml[7:-8]
            self.assertTrue(ssml in i18n.WRONG_CODE or ssml in i18n.CODE_EXPIRED)
        else:
            self.assertTrue(True)
        
        


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("authorization_with_no_phone"))
    suite.addTest(AlexaParticleTests("send_code"))
    suite.addTest(AlexaParticleTests("sign_in"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
