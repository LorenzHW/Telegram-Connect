import unittest
from unittest.mock import Mock, patch

from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded

from skill.helper_functions import remove_ssml_tags
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.setup_intent.setup_intent_request import setup_request
from skill_test.util import update_request, get_i18n_for_tests


class SetupIntentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = sb.lambda_handler()

    @patch("skill.intents.setup_intent.StateManager")
    @patch("skill.intents.setup_intent.PyrogramManager", spec=PyrogramManager)
    def test_setup_intent(self, mock_pyrogram_manager, mock_state_manager):
        for locale in ["en-US", "de-DE"]:
            setup_request["session"]["attributes"]["phone_code_hash"] = None
            setup_request["request"]["intent"]["slots"]["code"]["value"] = None
            mock_pyrogram_manager.send_code = Mock(return_value='random_phone_code_hash')
            mock_pyrogram_manager.is_authorized = False
            mock_pyrogram_manager.sign_in = Mock(return_value=None)
            mock_pyrogram_manager.return_value = mock_pyrogram_manager

            self._test_start_of_setup_intent(locale)
            self._test_user_provides_correct_code(locale)
            self._test_possible_problems_during_sign_in(locale, mock_pyrogram_manager)

    def _test_start_of_setup_intent(self, locale):
        req = update_request(setup_request, locale)

        event = self.handler(req, None)

        self.assertTrue(event.get("sessionAttributes").get("phone_code_hash") == 'random_phone_code_hash')
        self.assertEqual(event.get('response').get('directives')[0].get('type'), 'Dialog.ElicitSlot')

    def _test_user_provides_correct_code(self, locale):
        i18n = get_i18n_for_tests(locale)
        req = update_request(setup_request, locale)
        req["session"]["attributes"]["phone_code_hash"] = 'random_code_hash'
        req["request"]["intent"]["slots"]["code"]["value"] = 1234

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, i18n.SUCCESS_SETUP)

    def _test_possible_problems_during_sign_in(self, locale, mock_pyrogram_manager):
        i18n = get_i18n_for_tests(locale)
        req = update_request(setup_request, locale)
        code = 1234
        req["session"]["attributes"]["phone_code_hash"] = 'random_code_hash'
        req["request"]["intent"]["slots"]["code"]["value"] = code

        mock_pyrogram_manager.sign_in = Mock(side_effect=PhoneCodeInvalid())
        mock_pyrogram_manager.return_value = mock_pyrogram_manager
        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
        self.assertEqual(output, i18n.PHONE_CODE_INVALID.format(code))
        self.assertEqual(event.get('response').get('directives')[0].get('type'), 'Dialog.ElicitSlot')

        mock_pyrogram_manager.sign_in = Mock(side_effect=PhoneCodeExpired())
        mock_pyrogram_manager.return_value = mock_pyrogram_manager
        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
        self.assertEqual(output, i18n.PHONE_CODE_EXPIRED)

        mock_pyrogram_manager.sign_in = Mock(side_effect=SessionPasswordNeeded())
        mock_pyrogram_manager.return_value = mock_pyrogram_manager
        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
        self.assertEqual(output, i18n.TWO_STEP_ON)
