from src.skill.intents.generic_intent_handlery import GenericIntentHandler


class CustomIntentHandler(GenericIntentHandler):
    def __init__(self, locale):
        super().__init__(locale)