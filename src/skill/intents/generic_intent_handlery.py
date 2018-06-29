import random

from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.responses import ResponseOptions, statement, conversation


class GenericIntentHandler(object):
    def __init__(self, locale):
        self.i18n = LanguageModel(locale)
        self.response_options = ResponseOptions()

    ##############################
    # Required Intents
    ##############################
    def cancel_intent(self):
        goodbye = random.choice(self.i18n.GOODBYES)
        self.response_options.set_options(goodbye, goodbye)
        return statement(self.response_options)

    def help_intent(self):
        sess_attr = {'intent': {'name': 'help_intent'}}
        self.response_options.set_options(self.i18n.HELP_TITLE, self.i18n.HELP, sess_attr)
        return conversation(self.response_options)

    def stop_intent(self):
        goodbye = random.choice(self.i18n.GOODBYES)
        self.response_options.set_options(goodbye, goodbye)
        return statement(self.response_options)

    def on_launch(self, event, context):
        self.response_options.set_options(self.i18n.WELCOME_TITLE, self.i18n.WELCOME)
        return conversation(self.response_options)

    def fallback_intent(self, event, context):
        self.response_options.set_options(self.i18n.FALLBACK_TITLE, self.i18n.FALLBACK)
        return conversation(self.response_options)

    def yes_intent(self, event, context):
        ack = self.i18n.get_random_ack()
        self.response_options.set_options(ack, ack)
        return statement(self.response_options)

    def no_intent(self, event, context):
        ack = self.i18n.get_random_ack()
        self.response_options.set_options(ack, ack)
        return statement(self.response_options)

    def update_objects_on_new_session(self):
        pass

    def update_objects_on_new_lambda_call(self, locale):
        self.i18n = LanguageModel(locale)

    def get_previous_intent(self, event):
        previous_intent = None

        if 'attributes' in event['session']:
            if 'intent' in event['session']['attributes']:
                if event['session']['attributes']['intent']['name'] == 'help_intent':
                    previous_intent = 'help_intent'
                elif event['session']['attributes']['intent']['name'] == 'launch_intent':
                    previous_intent = 'launch_intent'

        return previous_intent

    def wrong_intent(self):
        title = self.i18n.WRONG_INTENT_TITLE
        body = self.i18n.WRONG_INTENT
        self.response_options.set_options(title, body)
        return statement(self.response_options)
