from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.utils import get_most_likely_name, send_telegram


class SendIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("SendIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        updated_intent = Intent("SendIntent", slots)
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = LanguageModel(handler_input.request_envelope.request.locale)

        for slot_name in slots:
            slot = slots[slot_name]
            if slot_name == "first_name" and slots["message"].value is None:
                if slot.value is None:
                    slot_to_elicit = "first_name"
                    speech_text = i18n.FIRST_NAME
                    reprompt = i18n.FIRST_NAME_REPROMPT
                else:
                    if not sess_attrs.get("FIRST_NAMES"):
                        # TODO: REQUEST INTO BACKEND: GETS USERS
                        contacts = self.telethon_service.get_potential_contacts(slot.value)
                        if len(contacts) == 1:
                            slot_to_elicit = "message"
                            speech_text = i18n.MESSAGE.format(contacts[0].first_name)
                        else:
                            slot_to_elicit = "first_name"
                            name_1 = contacts[0].first_name
                            name_2 = contacts[1].first_name
                            name_3 = contacts[2].first_name
                            speech_text = i18n.NO_CONTACT.format(name_1, name_2, name_3)
                            reprompt = i18n.NO_CONTACT_REPROMPT.format(name_1, name_2, name_3)
                            sess_attrs["FIRST_NAMES"] = [contact.first_name for contact in contacts]

                    else:
                        # Multiple contacts were found. Alexa provided three choices.
                        first_names = sess_attrs["FIRST_NAMES"]
                        name = get_most_likely_name(first_names, slot.value)

                        if name:
                            slot_to_elicit = "message"
                            speech_text = i18n.get_random_acceptance_ack() + ", " \
                                          + i18n.MESSAGE.format(name)
                            reprompt = i18n.get_random_dont_understand() + ", " \
                                       + i18n.MESSAGE.format(name)
                        else:
                            speech_text = i18n.MAX_NO_CONTACT
                            handler_input.response_builder.speak(
                                speech_text).set_should_end_session(True)
                            return handler_input.response_builder.response

                elicit_directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(elicit_directive)

            if slot.name == "message" and slot.value:
                send_telegram("NAME OF SEND TELEGRAM")
                speech_text = i18n.get_random_anyting_else()
                reprompt = i18n.FALLBACK
                sess_attrs.clear()

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(reprompt)

        return handler_input.response_builder.response
