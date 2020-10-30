import unittest
from unittest.mock import Mock

from skill.helper_functions import remove_ssml_tags
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.message_intent.message_request import message_request

mock_data = [
    {
        "name": 'Bello',
        "telegrams": [('This is the first message', 'Bello'), ('This is the second message', 'Bello')],
        "is_group": False
    },
    {
        "name": 'My Group',
        "telegrams": [('Group Message A', 'Chico'), ('Group Message B', 'Bello')],
        "is_group": True
    }
]

expected_results = [
    "<speak>You received new telegrams from: Bello<break time='200ms'/> and My Group<break time='200ms'/>. Bello wrote: This is the first message <break time='350ms'/>This is the second message<break time='2000ms'/> Do you want to hear the telegrams from your next contact?</speak>",
    "<speak>In My Group: Chico wrote: <break time=\'200ms\'/>Group Message A <break time=\'350ms\'/>Bello wrote: <break time=\'200ms\'/>Group Message B<break time=\'2000ms\'/> There are no more new telegrams. Bye for now.</speak>"
]


class MessageIntentTest(unittest.TestCase):
    def test_message(self):
        handler = sb.lambda_handler()

        for locale in ["en-US"]:
            i18n = get_i18n(locale, "America/Los_Angeles")
            req = self._update_request(message_request, locale)

            PyrogramManager.get_unread_telegrams = Mock(return_value=[])
            event = handler(req, None)
            output_text = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertTrue(i18n.NO_NEW_TELEGRAMS in output_text)

            PyrogramManager.get_unread_telegrams = Mock(return_value=mock_data)
            for new_telegrams_index in range(len(mock_data)):
                req["session"]["attributes"]["new_telegrams_index"] = new_telegrams_index
                event = handler(req, None)
                output_text = event.get('response').get('outputSpeech').get('ssml')
                self.assertEqual(output_text, expected_results[new_telegrams_index])

    def _update_request(self, request, locale):
        request["session"]["user"]["userId"] = "test_user"
        request["context"]["System"]["user"]["userId"] = "test_user"
        request["request"]["locale"] = locale
        return request
