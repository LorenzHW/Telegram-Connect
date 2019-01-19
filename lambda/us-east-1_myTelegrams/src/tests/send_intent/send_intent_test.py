import unittest

from src.tests.send_intent.send_requests import *
from src.tests.secret import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from lambda_function import sb



class AlexaParticleTests(unittest.TestCase):
    def test_send_request(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        send_request_1["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_request_1["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_request_1, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        # Remove random acknowledgment, a bit sloppy but ok..
        # Longest random ack is: 'Okey Dokey' with 10 chars
        # <speak> with 7 chars --> 17
        test_case = '<speak>{}</speak>'.format(i18n.FIRST_NAME)[17:]
        self.assertTrue(test_case in ssml)
        
        send_request_2["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_request_2["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_request_2, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.MESSAGE.format('Lorenz')))

        send_request_3["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_request_3["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_request_3, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml.split('.')[1][1:-8]
        self.assertTrue(test_case in i18n.ANYTHING_ELSE)

    def test_send_request_multiple_contacts_and_one_shot_intent(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        send_request_4["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_request_4["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_request_4, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml[-43:-8]
        self.assertTrue(test_case in i18n.NO_CONTACT)

        send_request_5["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        send_request_5["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(send_request_5, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml[-40:-8]
        self.assertTrue(test_case in i18n.MESSAGE.format('Lorenz'))
        

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("test_send_request"))
    suite.addTest(AlexaParticleTests("test_send_request_multiple_contacts_and_one_shot_intent"))
    runner = unittest.TextTestRunner()
    runner.run(suite)