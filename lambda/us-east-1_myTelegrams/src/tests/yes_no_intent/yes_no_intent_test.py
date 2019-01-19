import unittest

from src.tests.yes_no_intent.yes_requests import *
from src.tests.yes_no_intent.no_requests import *
from src.tests.secret import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from lambda_function import sb



class AlexaParticleTests(unittest.TestCase):
    def different_yes_intents(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # User wants to authorize: user did not add phone number
        yes_request_3["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_request_3["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_request_3, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.NO_PHONE))

        # User answered with not a number when Alexa is suggesting contacts in SendIntent
        yes_request_5["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_request_5["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_request_5, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        test_case = ssml[7:58]
        self.assertTrue(test_case in i18n.MAX_NO_CONTACT)

        # User answers yes on: "Do you want to reply?"
        yes_request_6["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_request_6["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_request_6, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[-29:-8]
        self.assertTrue(ssml in i18n.MESSAGE_2)
        
        # TODO: Add test on: "Is there anything else I can help you with?"

    def difficult_to_test_yes_intents(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # User wants to authorize: either user receives code
        # This breaks a lot, because we also send request into backend..
        yes_request_2["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_request_2["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_request_2, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.WHAT_IS_CODE))


        # User wants to listen to new telegrams
        # Difficult to test, cuz every time the test runs, I need an unread telegram
        yes_request_4["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        yes_request_4["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(yes_request_4, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        # TODO: cut string accordingly
        self.assertTrue(ssml in i18n.REPLY)
        

    def different_no_intents(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()

        # User answered No on question: "Welcome, u r not authorized. Authorize now?"
        no_request_2["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        no_request_2["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(no_request_2, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[-20:-8]
        self.assertTrue(ssml in i18n.BYE_FOR_NOW)

        # User answered No on question: "Welcome, do you want to hear your new Telegrams?"
        no_request_3["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        no_request_3["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(no_request_3, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        ssml = ssml[-92:-8]
        self.assertTrue(ssml in i18n.HELP_USER)

        # User answers no on: "Do you want to reply?" with only one unread conversation
        no_request_4["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        no_request_4["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(no_request_4, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertEqual(ssml, '<speak>{}</speak>'.format(i18n.NO_MORE_TELEGRAMS))

        # TODO: test if there are multiple conversations and user does not want to reply
        # TODO: Add User answered No on question: "Is there anything else I can help you with?

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("different_yes_intents"))
    suite.addTest(AlexaParticleTests("different_no_intents"))
    # suite.addTest(AlexaParticleTests("difficult_to_test_yes_intents"))
    runner = unittest.TextTestRunner()
    runner.run(suite)