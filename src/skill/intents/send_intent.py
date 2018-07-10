from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
# class SendIntentHandler(object):
#     def __init__(self, locale):
#         # TODO: I need to update language model on new lambda call (main.py) --> probably need to move this class to custom_intent_handler and work with inheritance
#         self.response_options = ResponseOptions()
#         self.slots = Slots()
#         self.service = DailyTelegramsService()
#         self.telethon_service = TelethonService()
#
#     def handle_intent(self, event, context):
#         slots = event['request']['intent']['slots']
#         slots = self.order_slots(slots)
#         sess_attr = self.get_session_attributes(event)
#
#         for slot in slots:
#             has_value = self.collect_slot_values(slot)
#             self.response_options.slots = self.slots.get_slots_in_list()
#
#             if slot['name'] == "first_name":
#                 if not has_value:
#                     self.response_options.title = "Works"
#                     self.response_options.body = "Okay, what is the first name of your contact?"
#                     slot_to_elicit = 'first_name'
#                 else:
#                     # TODO: REQUEST INTO BACKEND: GETS USERS
#                     if sess_attr and ['potential_contacts']:
#                         # TODO: compare slot value to contacts (percentage) pick most likely
#                         pass
#                     else:
#                         contacts = self.telethon_service.get_potential_contacts(slot['value'])
#
#                         if len(contacts) == 1:
#                             self.response_options.title = "Works"
#                             self.response_options.body = "Got it, what is the message for Tom?"
#                             slot_to_elicit = 'message'
#                         else:
#                             self.response_options.body = "Umm, I can't find any contact with that name. I found Tommy, Thomas, and Tod. To whom should I send the Telegram?"
#                             slot_to_elicit = 'first_name'
#                             sess_attr = {
#                                 'potential_contacts': {
#                                     'contact0': contacts[0].first_name,
#                                     'contact1': contacts[1].first_name,
#                                     'contact2': contacts[2].first_name,
#                                 },
#                             }
#                             self.response_options.session_attributes = sess_attr
#
#                 response = create_dialog_elicit_slot(self.response_options,
#                                                      'SendIntent',
#                                                      slot_to_elicit)
#
#             if slot['name'] == "message" and has_value:
#                 self.send_telegram()
#                 self.response_options.title = "Works"
#                 self.response_options.body = "Done. Is there anything else I can help you with?"
#                 response = conversation(self.response_options)
#
#         return response
#
#     def collect_slot_values(self, slot):
#         has_value = False
#
#         if 'value' in slot:
#             self.slots.update_slot(slot)
#             has_value = True
#
#         return has_value
#
#     def order_slots(self, slots):
#         slots = [slots['first_name'], slots['message']]
#         return slots
#
#     def send_telegram(self):
#         pass
#
#     def get_session_attributes(self, event):
#         if "attributes" in event['session']:
#             return event['session']['attributes']
#         else:
#             return None
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.services.telethon_service import TelethonService


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
                        # TODO: compare slot value to contacts (percentage) pick most likely
                        slot_to_elicit = "message"
                        speech_text = "Got it, what is the message for Tod?"

                elicit_directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(elicit_directive)

            if slot.name == "message" and slot.value:
                self.send_telegram()
                speech_text = "Done. Is there anything else I can help you with?"

        handler_input.response_builder.speak(speech_text).set_should_end_session(False)

        return handler_input.response_builder.response

    def send_telegram(self):
        pass
