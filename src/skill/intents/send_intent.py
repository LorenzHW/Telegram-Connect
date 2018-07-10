from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.models.general_models import Contact
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.parser import get_most_likely_contact


class SendIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("SendIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        updated_intent = Intent("SendIntent", slots)
        sess_attrs = handler_input.attributes_manager.session_attributes

        for slot_name in slots:
            slot = slots[slot_name]
            if slot_name == "first_name" and slots["message"].value is None:
                if slot.value is None:
                    slot_to_elicit = "first_name"
                    speech_text = "Okay, what is the first name of your contact?"
                else:
                    if not sess_attrs.get("CONTACT0"):
                        # TODO: REQUEST INTO BACKEND: GETS USERS
                        contacts = self.telethon_service.get_potential_contacts(slot.value)
                        if len(contacts) == 1:
                            slot_to_elicit = "message"
                            speech_text = "Got it, what is the message for Tom?"
                        else:
                            slot_to_elicit = "first_name"
                            speech_text = "Umm, I can't find any contact with that name. I found Tommy, Thomas, and Tod. To whom should I send the Telegram?"

                            for index, contact in enumerate(contacts):
                                sess_attrs["CONTACT" + str(index)] = contact.first_name
                    else:
                        # Multiple contacts were found. Alexa provided three choices.
                        contacts = self.reconstruct_contacts(sess_attrs)
                        contact = get_most_likely_contact(contacts, slot.value)

                        if contact:
                            slot_to_elicit = "message"
                            speech_text = "Got it, what is the message for {}?".format(
                                contact.first_name)
                        else:

                            handler_input.response_builder.speak(
                                "To risky bro").set_should_end_session(True)
                            return handler_input.response_builder.response

                elicit_directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(elicit_directive)

            if slot.name == "message" and slot.value:
                self.send_telegram()
                speech_text = "Done. Is there anything else I can help you with?"
                sess_attrs.clear()
                sess_attrs["PREV_INTENT"] = "SendIntent"

        handler_input.response_builder.speak(speech_text).set_should_end_session(False)

        return handler_input.response_builder.response

    def send_telegram(self):
        pass

    def reconstruct_contacts(self, sess_attrs):
        contacts = []

        for key in sess_attrs:
            if "CONTACT" in key:
                name = sess_attrs.get(key)
                contact = Contact(name)
                contacts.append(contact)
        return contacts
