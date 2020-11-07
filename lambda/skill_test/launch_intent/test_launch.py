import unittest
from unittest.mock import Mock, patch

from skill.helper_functions import remove_ssml_tags, ExploreIntents
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.launch_intent.launch_request import launch_request
from skill_test.util import update_request, TEST_USER_UNAUTHORIZED, TEST_USER_AUTHORIZED


class LaunchIntentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = sb.lambda_handler()

    def test_launch_intent(self):
        for locale in ["en-US"]:
            self._test_new_user_who_has_not_completed_setup(locale)
            self._test_user_who_has_no_new_telegrams(locale)
            self._test_user_who_has_unread_telegrams(locale)

    @patch("skill.telegram_connect.StateManager")
    @patch("skill.telegram_connect.PyrogramManager", spec=PyrogramManager)
    def _test_new_user_who_has_not_completed_setup(self, locale, mock_pyrogram_manager, mock_state_manager):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(launch_request, locale, TEST_USER_UNAUTHORIZED)
        mock_pyrogram_manager.is_authorized = Mock(return_value=False)
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, i18n.NEW_SETUP)
        self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_SETUP_INTENT)

    @patch("skill.telegram_connect.StateManager")
    @patch("skill.telegram_connect.PyrogramManager", spec=PyrogramManager)
    def _test_user_who_has_no_new_telegrams(self, locale, mock_pyrogram_manager, mock_state_manager):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(launch_request, locale, "TEST_USER_AUTHORIZED")
        mock_pyrogram_manager.is_authorized = Mock(return_value=True)
        mock_pyrogram_manager.get_unread_dialogs = Mock(return_value=[])
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertTrue(i18n.WELCOME_BACK + ' ' + i18n.NO_NEW_TELEGRAMS in output)

    @patch("skill.telegram_connect.StateManager")
    @patch("skill.telegram_connect.PyrogramManager", spec=PyrogramManager)
    def _test_user_who_has_unread_telegrams(self, locale, mock_pyrogram_manager, mock_state_manager):
        unread_telegrams = ['something']
        req = update_request(launch_request, locale, TEST_USER_AUTHORIZED)
        mock_pyrogram_manager.is_authorized = Mock(return_value=True)
        mock_pyrogram_manager.get_unread_dialogs = Mock(return_value=unread_telegrams)
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)

        self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_MESSAGE_INTENT)
        self.assertEqual(event.get('sessionAttributes').get('unread_dialogs'), unread_telegrams)
