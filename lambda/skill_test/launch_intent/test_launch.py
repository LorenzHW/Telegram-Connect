import unittest
from unittest.mock import Mock, PropertyMock

from skill.helper_functions import remove_ssml_tags, ExploreIntents
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.launch_intent.launch_request import launch_request


class LaunchIntentTest(unittest.TestCase):
    def test_launch(self):
        handler = sb.lambda_handler()
        for locale in ["en-US"]:
            i18n = get_i18n(locale, "America/Los_Angeles")
            req = self._update_request(launch_request, locale)

            event = handler(req, None)
            output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertEqual(output, i18n.NEW_SETUP)
            self.assertEqual(event.get("sessionAttributes").get("explore_intent"), ExploreIntents.EXPLORE_SETUP_INTENT)

            PyrogramManager.is_authorized = PropertyMock(return_value=True)
            PyrogramManager.get_unread_telegrams = Mock(return_value=[])
            event = handler(req, None)
            output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertTrue(i18n.WELCOME_BACK + ' ' + i18n.NO_NEW_TELEGRAMS in output)

            unread_telegrams = ['something']
            PyrogramManager.get_unread_telegrams = Mock(return_value=unread_telegrams)
            event = handler(req, None)
            self.assertEqual(event.get("sessionAttributes").get("explore_intent"),
                             ExploreIntents.EXPLORE_MESSAGE_INTENT)
            self.assertEqual(event.get('sessionAttributes').get('new_telegrams'), unread_telegrams)

    def _update_request(self, request, locale):
        request["session"]["user"]["userId"] = "test_user"
        request["context"]["System"]["user"]["userId"] = "test_user"
        request["request"]["locale"] = locale
        return request
