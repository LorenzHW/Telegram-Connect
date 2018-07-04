from src.skill.intents.custom_intent_handler import CustomIntentHandler


class IntentRouter(object):
    def __init__(self, locale):
        self.custom_intent_handler = CustomIntentHandler(locale)

    def route_launch_request(self, event, context):
        return self.custom_intent_handler.on_launch(event, context)

    def route_intent_request(self, event, context):
        intent_name = event['request']['intent']['name']

        # Custom Intents
        if intent_name == "MessageIntent" or intent_name == "SendIntent" or intent_name == "AuthorizationIntent":
            return self.custom_intent_handler.delegate_intent(intent_name, event, context)

        # Required Intents
        if intent_name == "AMAZON.CancelIntent":
            return self.custom_intent_handler.cancel_intent()

        if intent_name == "AMAZON.HelpIntent":
            return self.custom_intent_handler.help_intent()

        if intent_name == "AMAZON.FallbackIntent":
            return self.custom_intent_handler.fallback_intent(event, context)

        if intent_name == "AMAZON.StopIntent":
            return self.custom_intent_handler.stop_intent()

        if intent_name == "AMAZON.YesIntent":
            return self.custom_intent_handler.yes_intent(event, context)

        if intent_name == "AMAZON.NoIntent":
            return self.custom_intent_handler.no_intent(event, context)
