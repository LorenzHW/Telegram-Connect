import unittest
from unittest.mock import Mock, PropertyMock

from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded

from skill.helper_functions import remove_ssml_tags
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.setup_intent.setup_intent_request import setup_request
from skill_test.util import update_request, TEST_USER_UNAUTHORIZED, TEST_USER_AUTHORIZED


class SetupIntentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = sb.lambda_handler()

    def test_setup_intent(self):
        # for locale in ["en-US"]:
        # self._test_setup_intent_with_mock_values(locale)
        self._test_setup_real()

    def _test_setup_intent_with_mock_values(self, locale):
        PyrogramManager.send_code = Mock(return_value='random_phone_code_hash')
        PyrogramManager.is_authorized = PropertyMock(return_value=False)
        PyrogramManager.sign_in = Mock(return_value=None)

        self._test_start_of_setup_intent(locale)
        self._test_user_provides_correct_code(locale)
        self._test_possible_problems_during_sign_in(locale)

    def _test_start_of_setup_intent(self, locale):
        req = update_request(setup_request, locale, TEST_USER_UNAUTHORIZED)

        event = self.handler(req, None)

        self.assertTrue(event.get("sessionAttributes").get("phone_code_hash") == 'random_phone_code_hash')
        self.assertEqual(event.get('response').get('directives')[0].get('type'), 'Dialog.ElicitSlot')

    def _test_user_provides_correct_code(self, locale):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(setup_request, locale, TEST_USER_UNAUTHORIZED)
        req["session"]["attributes"]["phone_code_hash"] = 'random_code_hash'
        req["request"]["intent"]["slots"]["code"]["value"] = 1234

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, i18n.SUCCESS_SETUP)

    def _test_possible_problems_during_sign_in(self, locale):
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(setup_request, locale, TEST_USER_UNAUTHORIZED)
        code = 1234
        req["session"]["attributes"]["phone_code_hash"] = 'random_code_hash'
        req["request"]["intent"]["slots"]["code"]["value"] = code

        PyrogramManager.sign_in = Mock(side_effect=PhoneCodeInvalid())
        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
        self.assertEqual(output, i18n.PHONE_CODE_INVALID.format(code))
        self.assertEqual(event.get('response').get('directives')[0].get('type'), 'Dialog.ElicitSlot')

        PyrogramManager.sign_in = Mock(side_effect=PhoneCodeExpired())
        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
        self.assertEqual(output, i18n.PHONE_CODE_EXPIRED)

        PyrogramManager.sign_in = Mock(side_effect=SessionPasswordNeeded())
        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
        self.assertEqual(output, i18n.TWO_STEP_ON)

    def _test_setup_real(self):
        """
        This is not a Unit test. This method will help to create a dynamo db database entry with id: 'test_user_authorized'
        You need to provide your real phone number and the code you receive in Telegram once you execute this method.

        This user can then be used to actually fetch data from the Telegram API like in the PyrogramTest
        """
        locale = 'en-US'
        i18n = get_i18n(locale, "America/Los_Angeles")
        req = update_request(setup_request, locale, TEST_USER_AUTHORIZED)
        req["session"]["attributes"]["phone_num"] = input('Type in your phone number (e.g.: 49123456)')

        event = self.handler(req, None)

        req["session"]["attributes"]["phone_code_hash"] = event.get("sessionAttributes").get("phone_code_hash")
        req["request"]["intent"]["slots"]["code"]["value"] = input('Check your phone for a code. What is the code?')

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, i18n.SUCCESS_SETUP)
        self.assertTrue(event.get("sessionAttributes").get("phone_code_hash") is not None)
