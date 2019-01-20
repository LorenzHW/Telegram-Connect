from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.daily_telegrams_service import DailyTelegramsService
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.exceptions import TelethonException, handle_telethon_error_response
from src.skill.utils.constants import Constants


class SpeedIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("SpeedIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        updated_intent = Intent("SpeedIntent", slots)
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = Constants.i18n
        daily_telegrams_service = DailyTelegramsService()
        telethon_service = TelethonService()

        for slot_name in slots:
            slot = slots[slot_name]
            if slot_name == "speed_dial_number" and slots.get("message").value is None:
                if slot.value is None:
                    slot_to_elicit = "speed_dial_number"
                    speech_text = i18n.SPEED_DIAL
                    reprompt = i18n.SPEED_DIAL_REPROMPT
                else:
                    slot_to_elicit = "message"
                    first_name = daily_telegrams_service.get_firstname_for_speed_dial_number(
                        slot.value)
                    if first_name:
                        try:
                            contacts = telethon_service.get_potential_contacts(first_name)
                        except TelethonException as error:
                            return handle_telethon_error_response(error, handler_input)

                        if len(contacts) > 1:
                            speech_text = i18n.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL
                            handler_input.response_builder.speak(speech_text) \
                                .set_should_end_session(True)
                            return handler_input.response_builder.response

                        speech_text = i18n.get_random_acceptance_ack() + ", " \
                                      + i18n.MESSAGE.format(contacts[0].first_name)
                        reprompt = i18n.get_random_dont_understand() + ", " \
                                   + i18n.MESSAGE.format(contacts[0].first_name)

                        sess_attrs["FIRST_NAMES"] = [contacts[0].first_name]
                        sess_attrs["TELETHON_ENTITY_ID"] = contacts[0].entity_id
                    else:
                        speech_text = i18n.NO_SPEED_DIAL_CONTACT
                        reprompt = i18n.FALLBACK
                        handler_input.response_builder.speak(speech_text) \
                            .set_should_end_session(False).ask(reprompt)

                        return handler_input.response_builder.response
                elicit_directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(elicit_directive)

            if slot.name == "message" and slot.value:
                try:
                    entity_id = sess_attrs.get("TELETHON_ENTITY_ID")
                    self.telethon_service.send_telegram(entity_id, slot.value)
                except TelethonException as error:
                    return handle_telethon_error_response(error, handler_input)

                speech_text = i18n.get_random_anyting_else()
                reprompt = i18n.FALLBACK
                sess_attrs.clear()

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(reprompt)

        return handler_input.response_builder.response
