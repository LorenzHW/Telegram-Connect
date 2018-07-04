from src.skill.intents.generic_intent_handler import GenericIntentHandler
from src.skill.intents.send_intent_handler import SendIntentHandler


class CustomIntentHandler(GenericIntentHandler):
    def __init__(self, locale):
        super().__init__(locale)
        self.send_intent_handler = SendIntentHandler(locale)

    def delegate_intent(self, intent_name, event, context):
        if intent_name == "SendIntent":
            return self.send_intent_handler.handle_intent(event, context)
