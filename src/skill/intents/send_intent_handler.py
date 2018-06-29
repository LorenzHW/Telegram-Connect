from src.skill.intents.custom_intent_handler import CustomIntentHandler


class SendIntent(CustomIntentHandler):
    def __init__(self, locale):
        super().__init__(locale)