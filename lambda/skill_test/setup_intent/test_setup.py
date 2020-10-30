import unittest
from unittest.mock import Mock, PropertyMock

from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded

from skill.helper_functions import remove_ssml_tags
from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.telegram_connect import sb
from skill_test.setup_intent.setup_intent_request import setup_request


class SetupIntentTest(unittest.TestCase):
    def test_setup(self):
        self._test_setup_mock()
        # self._test_setup_real()

    def _test_setup_real(self):
        handler = sb.lambda_handler()
        for locale in ["en-US"]:
            i18n = get_i18n(locale, "America/Los_Angeles")
            req = self._update_request(setup_request, locale)

            event = handler(req, None)
            self.assertTrue(event.get("sessionAttributes").get("phone_code_hash") is not None)

            req["session"]["attributes"]["phone_code_hash"] = event.get("sessionAttributes").get("phone_code_hash")
            code = "TODO"
            req["request"]["intent"]["slots"]["code"]["value"] = code
            if req["request"]["intent"]["slots"]["code"]["value"] != "TODO":
                event = handler(req, None)
                output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
                self.assertEqual(output, i18n.SUCCESS_SETUP)

    def _test_setup_mock(self):
        handler = sb.lambda_handler()
        for locale in ["en-US"]:
            i18n = get_i18n(locale, "America/Los_Angeles")
            req = self._update_request(setup_request, locale)

            PyrogramManager.send_code = Mock(return_value='random_phone_code_hash')
            PyrogramManager.is_authorized = PropertyMock(return_value=True)
            event = handler(req, None)
            self.assertTrue(event.get("sessionAttributes").get("phone_code_hash") == 'random_phone_code_hash')
            self.assertEqual(event.get('response').get('directives')[0].get('type'), 'Dialog.ElicitSlot')

            code = 1234
            req["session"]["attributes"]["phone_code_hash"] = event.get("sessionAttributes").get("phone_code_hash")
            req["request"]["intent"]["slots"]["code"]["value"] = code
            PyrogramManager.sign_in = Mock(return_value=None)
            event = handler(req, None)
            output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertEqual(output, i18n.SUCCESS_SETUP)

            PyrogramManager.sign_in = Mock(side_effect=PhoneCodeInvalid())
            event = handler(req, None)
            output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertEqual(output, i18n.PHONE_CODE_INVALID.format(code))
            self.assertEqual(event.get('response').get('directives')[0].get('type'), 'Dialog.ElicitSlot')

            PyrogramManager.sign_in = Mock(side_effect=PhoneCodeExpired())
            event = handler(req, None)
            output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertEqual(output, i18n.PHONE_CODE_EXPIRED)

            PyrogramManager.sign_in = Mock(side_effect=SessionPasswordNeeded())
            event = handler(req, None)
            output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))
            self.assertEqual(output, i18n.TWO_STEP_ON)

    def _update_request(self, request, locale):
        request["session"]["user"]["userId"] = "test_user"
        request["context"]["System"]["user"]["userId"] = "test_user"
        request["request"]["locale"] = locale
        return request
