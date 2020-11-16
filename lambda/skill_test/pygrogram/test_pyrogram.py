import json
import unittest

from ask_sdk_core.attributes_manager import AttributesManager
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill import CustomSkill
from ask_sdk_model import RequestEnvelope

from skill.helper_functions import remove_ssml_tags
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.state_manager import StateManager
from skill.telegram_connect import sb
from skill_test.message_intent.message_request import message_request
from skill_test.setup_intent.setup_intent_request import setup_request
from skill_test.util import update_request, get_i18n_for_tests


class PyrogramTest(unittest.TestCase):
    """
    This is not a real Unit-test. However you can use this class to actually couple a test user with the Telegram API.
    Then you execute the methods inside PyrogramManager for real instead of mocking them.

    First you will need to run through the SetupIntent in order to get that user.
    """

    def setUp(self) -> None:
        skill = CustomSkill(skill_configuration=sb.skill_configuration)
        req = update_request(message_request, 'en-US')
        request_envelope = skill.serializer.deserialize(payload=json.dumps(req), obj_type=RequestEnvelope)
        attributes_manager = AttributesManager(request_envelope=request_envelope,
                                               persistence_adapter=skill.persistence_adapter)
        self.handler_input = HandlerInput(request_envelope, attributes_manager)
        self.handler = sb.lambda_handler()

    def test_pyrogram_manager(self):
        self.pyrogram_manager = PyrogramManager(StateManager(self.handler_input))
        if not self.pyrogram_manager.is_authorized:
            self.execute_setup_intent()
            self.pyrogram_manager = PyrogramManager(StateManager(self.handler_input))

        dialogs = self.pyrogram_manager.get_unread_dialogs()

    def execute_setup_intent(self):
        """
        This method will help to create a dynamo db database entry with id: 'test_user_authorized'
        You need to provide your real phone number and the code you receive in Telegram once you execute this method.

        This user can then be used to actually fetch data from the Telegram API like in the PyrogramTest
        """
        locale = 'en-US'
        i18n = get_i18n_for_tests(locale)
        req = update_request(setup_request, locale)
        req["session"]["user"]["userId"] = "AUTHORIZED_USER"
        req["context"]["System"]["user"]["userId"] = "AUTHORIZED_USER"

        req["session"]["attributes"]["phone_num"] = input('Type in your phone number (e.g.: 49123456)')

        event = self.handler(req, None)

        req["session"]["attributes"]["phone_code_hash"] = event.get("sessionAttributes").get("phone_code_hash")
        req["request"]["intent"]["slots"]["code"]["value"] = input('Check your phone for a code. What is the code?')

        event = self.handler(req, None)
        output = remove_ssml_tags(event.get('response').get('outputSpeech').get('ssml'))

        self.assertEqual(output, i18n.SUCCESS_SETUP)
        self.assertTrue(event.get("sessionAttributes").get("phone_code_hash") is not None)
