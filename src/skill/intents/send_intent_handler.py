from src.skill.utils.responses import ResponseOptions, statement


class SendIntentHandler(object):
    def __init__(self, locale):
        self.response_options = ResponseOptions()

    def handle_intent(self, event, context):
        self.response_options.set_options("Works", "Works")
        return
