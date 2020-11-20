import unittest
from unittest.mock import Mock, patch

from skill.helper_functions import remove_ssml_tags, ExploreIntents
from skill.interceptors import StateRequestInterceptor
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.launch_intent.launch_request import launch_request
from skill_test.util import update_request, get_i18n_for_tests


class LaunchIntentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = sb.lambda_handler()
        StateRequestInterceptor.process = Mock(return_value=[])

    @patch("skill.telegram_connect.StateManager")
    @patch("skill.telegram_connect.PyrogramManager", spec=PyrogramManager)
    def test_launch_intent(self, mock_pyrogram_manager, mock_state_manager):
        for locale in ["en-US", "de-DE"]:
            self._test_new_user_who_has_not_completed_setup(locale, mock_pyrogram_manager)
            self._test_user_who_has_no_new_telegrams(locale, mock_pyrogram_manager)
            self._test_user_who_has_unread_telegrams(locale, mock_pyrogram_manager)

    def _test_new_user_who_has_not_completed_setup(self, locale, mock_pyrogram_manager):
        i18n = get_i18n_for_tests(locale)
        req = update_request(launch_request, locale)
        mock_pyrogram_manager.is_authorized = Mock(return_value=False)
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, remove_ssml_tags(i18n.NEW_SETUP))
        self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_SETUP_INTENT)

    def _test_user_who_has_no_new_telegrams(self, locale, mock_pyrogram_manager):
        i18n = get_i18n_for_tests(locale)
        req = update_request(launch_request, locale)
        mock_pyrogram_manager.is_authorized = Mock(return_value=True)
        mock_pyrogram_manager.get_unread_dialogs = Mock(return_value=[])
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertTrue(i18n.WELCOME_BACK + ' ' + i18n.NO_NEW_TELEGRAMS in output)

    def _test_user_who_has_unread_telegrams(self, locale, mock_pyrogram_manager):
        unread_telegrams = ['something']
        req = update_request(launch_request, locale)
        mock_pyrogram_manager.is_authorized = Mock(return_value=True)
        mock_pyrogram_manager.get_unread_dialogs = Mock(return_value=unread_telegrams)
        mock_pyrogram_manager.return_value = mock_pyrogram_manager

        event = self.handler(req, None)

        self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_MESSAGE_INTENT)
        self.assertEqual(event.get('sessionAttributes').get('unread_dialogs'), unread_telegrams)
