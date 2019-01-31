import unittest

from src.tests.reply_intent.reply_requests import *
from src.tests.tokens import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants
from src.skill.utils.utils import set_language_model
from lambda_function import sb



class ReplyIntentTest(unittest.TestCase):
    
    def reply_or_next_telegram(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()
        
        # A: 'You got new Telegrams from Michael. Michael wrote... Reply or next Telegram?
        # U: 'Reply'
        reply_on_first_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        reply_on_first_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(reply_on_first_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-29:-8] in i18n.MESSAGE_2)

    def reply_on_last(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        # A: "Reply, send telegram, or stop?"
        # U: "Reply"
        reply_on_last_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        reply_on_last_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(reply_on_last_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-29:-8] in i18n.MESSAGE_2)

        # A: "Telegram?"
        # U: "Sup bro"
        message_for_reply_on_last_telegram["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        message_for_reply_on_last_telegram["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(message_for_reply_on_last_telegram, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[-40:-8] in i18n.NO_TELEGRAMS)

    def no_telethon_ids(self):
        i18n = Constants.i18n
        handler = sb.lambda_handler()

        no_telethon_ids["context"]["System"]["user"]["accessToken"] = VALID_TOKEN
        no_telethon_ids["session"]["user"]["accessToken"] = VALID_TOKEN
        event = handler(no_telethon_ids, None)
        ssml = event.get('response').get('outputSpeech').get('ssml')
        self.assertTrue(ssml[7:-8] in i18n.NO_TELETHON_ID)
        

if __name__ == "__main__":
    set_language_model('en-US', True)
    Constants.ACCESS_TOKEN = VALID_TOKEN

    suite = unittest.TestSuite()
    suite.addTest(ReplyIntentTest("reply_or_next_telegram"))
    suite.addTest(ReplyIntentTest("reply_on_last"))
    suite.addTest(ReplyIntentTest("no_telethon_ids"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
