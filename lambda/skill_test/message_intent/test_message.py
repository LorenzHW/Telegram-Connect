import unittest
from unittest.mock import Mock, PropertyMock, patch

from skill.helper_functions import remove_ssml_tags
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.message_intent.message_request import message_request
from skill_test.util import update_request, get_i18n_for_tests

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

expected_results = {
    "de-DE": [
        "<speak>Du hast neue Telegramme erhalten von: Bello<break time='200ms'/> und My Group<break time='200ms'/>. Bello schrieb: This is the first message <break time='350ms'/>This is the second message<break time='2000ms'/> Möchtest du die Telegramme vom nächsten Kontakt hören?</speak>",
        "<speak>In My Group: Chico schrieb: <break time='200ms'/>Group Message A <break time='350ms'/>Bello schrieb: <break time='200ms'/>Group Message B<break time='2000ms'/> Es gibt keine weiteren Telegramme. Bis später.</speak>"
    ],
    "en-US": [
        "<speak>You received new telegrams from: Bello<break time='200ms'/> and My Group<break time='200ms'/>. Bello wrote: This is the first message <break time='350ms'/>This is the second message<break time='2000ms'/> Do you want to hear the telegrams from your next contact?</speak>",
        "<speak>In My Group: Chico wrote: <break time=\'200ms\'/>Group Message A <break time=\'350ms\'/>Bello wrote: <break time=\'200ms\'/>Group Message B<break time=\'2000ms\'/> There are no more new telegrams. Bye for now.</speak>"
    ]
}



class MessageIntentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = sb.lambda_handler()

    @patch("skill.intents.message_intent.StateManager")
    @patch("skill.intents.message_intent.PyrogramManager", spec=PyrogramManager)
    def test_message_intent(self, mock_pyrogram_manager, mock_state_manager):
        for locale in ["en-US", "de-DE"]:
            mock_pyrogram_manager.is_authorized = True
            mock_pyrogram_manager.return_value = mock_pyrogram_manager

            self.test_when_user_has_no_new_telegrams(locale, mock_pyrogram_manager)
            self.test_when_user_has_new_telegrams(locale, mock_pyrogram_manager)

    def test_when_user_has_no_new_telegrams(self, locale, mock_pyrogram_manager):
        i18n = get_i18n_for_tests(locale)
        req = update_request(message_request, locale)
        mock_pyrogram_manager.get_unread_dialogs = Mock(return_value=[])
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)
        output_text = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertTrue(i18n.NO_NEW_TELEGRAMS in output_text)

    def test_when_user_has_new_telegrams(self, locale, mock_pyrogram_manager):
        req = update_request(message_request, locale)
        mock_pyrogram_manager.get_unread_dialogs = Mock(return_value=mock_data)
        mock_pyrogram_manager.read_history = Mock(return_value=True)
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        for new_telegrams_index in range(len(mock_data)):
            req["session"]["attributes"]["unread_dialog_index"] = new_telegrams_index

            event = self.handler(req, None)
            output_text = event.get('response').get('outputSpeech').get('ssml')

            self.assertEqual(output_text, expected_results[locale][new_telegrams_index])
