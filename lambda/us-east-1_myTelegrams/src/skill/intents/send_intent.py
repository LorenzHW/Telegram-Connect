from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.exceptions import TelethonException, handle_telethon_error_response
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import SpeedDialException, AccountException
from src.skill.utils.utils import handle_speed_dial_number_input, send_telegram, parse_spoken_numbers_to_integers, check_for_account
from src.skill.services.daily_telegrams_service import DailyTelegramsService


class SendIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        if is_intent_name("SendIntent")(handler_input):
            slots = handler_input.request_envelope.request.intent.slots
            if slots.get('message').value and not slots.get('first_name').value:
                return False
            return True

    def handle(self, handler_input):
        try:
            check_for_account(handler_input)
        except AccountException as error:
            return handler_input.response_builder \
                .speak(error.args[0]).set_should_end_session(True).response

        slots = handler_input.request_envelope.request.intent.slots
        updated_intent = Intent("SendIntent", slots)
        sess_attrs = handler_input.attributes_manager.session_attributes
        locale = handler_input.request_envelope.request.locale
        i18n = Constants.i18n

        for slot_name in slots:
            slot = slots[slot_name]
            if slot_name == "first_name" and slots["message"].value is None:
                if slot.value is None:
                    slot_to_elicit = "first_name"
                    speech_text = i18n.FIRST_NAME
                    reprompt = i18n.FIRST_NAME_REPROMPT
                else:
                    if not sess_attrs.get("FIRST_NAMES"):
                        if locale == 'de-DE':
                            # On German Alexa we get "vier" if user says a speed dial number
                            # On English Alexa we get "4"... --> need that also for German
                            slot.value = parse_spoken_numbers_to_integers(slot.value)

                        is_speed_dial = slot.value.isdigit()

                        if is_speed_dial:
                            try:
                                num = int(slot.value)
                                speech_text, reprompt, slot_to_elicit = \
                                    handle_speed_dial_number_input(
                                        num, sess_attrs, i18n)
                            except SpeedDialException as error:
                                return handler_input.response_builder \
                                    .speak(error.args[0]).set_should_end_session(True).response
                        else:
                            speech_text, reprompt, slot_to_elicit = self \
                                .handle_first_name_input(slot.value, sess_attrs, i18n)
                    else:
                        one_two_or_three = slots.get("one_two_or_three")

                        if one_two_or_three.value not in ["1", "2", "3"]:
                            speech_text = i18n.MAX_NO_CONTACT
                            handler_input.response_builder\
                                .speak(speech_text).set_should_end_session(True)
                            return handler_input.response_builder.response

                        speech_text, reprompt = self \
                            .get_users_choice(one_two_or_three, i18n, sess_attrs)
                        slot_to_elicit = "message"

                directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(directive)

            if slot.name == "message" and slot.value:
                try:
                    m = slot.value
                    speech_text, reprompt = send_telegram(m, sess_attrs, i18n)
                except TelethonException as error:
                    return handle_telethon_error_response(error, handler_input)

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(reprompt)

        return handler_input.response_builder.response

    def provide_choices(self, contacts, i18n):
        name_1 = contacts[0].first_name
        name_2 = contacts[1].first_name

        if len(contacts) == 3:
            name_3 = contacts[2].first_name
            speech_text = i18n.NO_CONTACT.format(name_1, name_2, name_3)
            reprompt = i18n.NO_CONTACT_REPROMPT.format(name_1, name_2, name_3)
        else:
            speech_text = i18n.NO_CONTACT_2.format(name_1, name_2)
            reprompt = i18n.NO_CONTACT_REPROMPT_2.format(name_1, name_2)
        return speech_text, reprompt

    def get_users_choice(self, one_two_or_three, i18n, sess_attrs):
        index = int(one_two_or_three.value) - 1
        telethon_id = sess_attrs.get("TELETHON_IDS")[index]
        sess_attrs["TELETHON_ENTITY_ID"] = telethon_id

        name = sess_attrs["FIRST_NAMES"][index]
        speech_text = i18n.MESSAGE.format(name)
        reprompt = i18n.MESSAGE_REPROMPT.format(name)
        return speech_text, reprompt

    def handle_first_name_input(self, first_name, sess_attrs, i18n):
        contacts = self.telethon_service.get_potential_contacts(first_name)

        if len(contacts) == 1:
            c = contacts[0]
            slot_to_elicit = "message"
            sess_attrs["TELETHON_ENTITY_ID"] = c.entity_id
            speech_text = i18n.MESSAGE.format(c.first_name)
            reprompt = i18n.MESSAGE_REPROMPT.format(c.first_name)
        else:
            slot_to_elicit = "one_two_or_three"
            speech_text, reprompt = self.provide_choices(contacts, i18n)
            sess_attrs["FIRST_NAMES"] = [c.first_name for c in contacts]
            sess_attrs["TELETHON_IDS"] = [c.entity_id for c in contacts]

        return (speech_text, reprompt, slot_to_elicit)
