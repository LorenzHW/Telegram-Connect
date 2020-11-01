import unittest
from unittest.mock import Mock, PropertyMock

from skill.helper_functions import remove_ssml_tags
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.message_intent.message_request import message_request
from skill_test.util import update_request, TEST_USER_AUTHORIZED

mock_data = [
    {
        "name": 'Bello',
        "telegrams": [('This is the first message', 'Bello'), ('This is the second message', 'Bello')],
        "is_group": False,
        "chat_id": "12341234"
    },
    {
        "name": 'My Group',
        "telegrams": [('Group Message A', 'Chico'), ('Group Message B', 'Bello')],
        "is_group": True,
        "chat_id": "12341234"
    }
]

expected_results = [
    "<speak>You received new telegrams from: Bello<break time='200ms'/> and My Group<break time='200ms'/>. Bello wrote: This is the first message <break time='350ms'/>This is the second message<break time='2000ms'/> Do you want to hear the telegrams from your next contact?</speak>",
    "<speak>In My Group: Chico wrote: <break time=\'200ms\'/>Group Message A <break time=\'350ms\'/>Bello wrote: <break time=\'200ms\'/>Group Message B<break time=\'2000ms\'/> There are no more new telegrams. Bye for now.</speak>"
]


class MessageIntentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = sb.lambda_handler()

    def test_message_intent(self):
        for locale in ["en-US"]:
            PyrogramManager.is_authorized = PropertyMock(return_value=True)
            self.test_when_user_has_new_telegrams(locale)
            self.test_when_user_has_new_telegrams(locale)

    def test_when_user_has_no_new_telegrams(self, locale):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(message_request, locale, TEST_USER_AUTHORIZED)
        PyrogramManager.get_unread_telegrams = Mock(return_value=[])

        event = self.handler(req, None)
        output_text = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertTrue(i18n.NO_NEW_TELEGRAMS in output_text)

    def test_when_user_has_new_telegrams(self, locale):
        req = update_request(message_request, locale, TEST_USER_AUTHORIZED)
        PyrogramManager.get_unread_telegrams = Mock(return_value=mock_data)
        PyrogramManager.read_history = Mock(return_value=True)

        for new_telegrams_index in range(len(mock_data)):
            req["session"]["attributes"]["new_telegrams_index"] = new_telegrams_index

            event = self.handler(req, None)
            output_text = event.get('response').get('outputSpeech').get('ssml')

            self.assertEqual(output_text, expected_results[new_telegrams_index])
