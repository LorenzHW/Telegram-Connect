import unittest
from unittest.mock import Mock, PropertyMock

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
            self.test_new_user_who_has_not_completed_setup(locale)
            self.test_user_who_has_no_new_telegrams(locale)
            self.test_user_who_has_unread_telegrams(locale)

    def test_new_user_who_has_not_completed_setup(self, locale):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(launch_request, locale, TEST_USER_UNAUTHORIZED)

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, i18n.NEW_SETUP)
        self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_SETUP_INTENT)

    def test_user_who_has_no_new_telegrams(self, locale):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(launch_request, locale, TEST_USER_AUTHORIZED)
        PyrogramManager.is_authorized = PropertyMock(return_value=True)
        PyrogramManager.get_unread_telegrams = Mock(return_value=[])

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertTrue(i18n.WELCOME_BACK + ' ' + i18n.NO_NEW_TELEGRAMS in output)

    def test_user_who_has_unread_telegrams(self, locale):
        unread_telegrams = ['something']
        req = update_request(launch_request, locale, TEST_USER_AUTHORIZED)
        PyrogramManager.is_authorized = PropertyMock(return_value=True)
        PyrogramManager.get_unread_telegrams = Mock(return_value=unread_telegrams)

        event = self.handler(req, None)

        self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_MESSAGE_INTENT)
        self.assertEqual(event.get('sessionAttributes').get('new_telegrams'), unread_telegrams)
