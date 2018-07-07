##############################
# Builders
##############################


def build_plain_speech(body):
    speech = {"type": "PlainText", "text": body}
    return speech


def build_ssml(body):
    speech = {"type": "SSML", "ssml": "<speak>" + body + "</speak>"}
    return speech


def build_response(message, session_attributes=None):
    response = {"version": "1.0", "sessionAttributes": session_attributes, "response": message}
    return response


def build_simple_card(title, body=None):
    card = {"type": "Simple", "title": title, "content": body}
    return card


def build_standard_card(title, images):
    card = {"type": "Standard", "title": title}

    if images:
        card["image"] = images

    return card


def builld_link_account_card(title, body):
    card = {"type": "LinkAccount", "title": title, "content": body}
    return card


def build_correct_card_type(options):
    if options.images is not None:
        card = build_standard_card(options.title, options.images)
    elif options.link_account_card:
        card = builld_link_account_card(options.title, options.body)
    else:
        card = build_simple_card(options.title, options.body)

    return card


def build_correct_output_speech(options):
    if options.ssml:
        output_speech = build_ssml(options.ssml)
    else:
        output_speech = build_plain_speech(options.body)

    return output_speech


def build_correct_reprompt(options):
    output_speech = build_correct_output_speech(options)
    reprompt = {"outputSpeech": output_speech}
    return reprompt


##############################
# Responses
##############################
def conversation(conversation_options):
    response = {"shouldEndSession": False,
                "outputSpeech": build_correct_output_speech(conversation_options),
                "card": build_correct_card_type(conversation_options)}

    if conversation_options.reprompt:
        response["reprompt"] = build_correct_reprompt(conversation_options)

    return build_response(response, session_attributes=conversation_options.session_attributes)


def statement(statement_options):
    response = {"shouldEndSession": True,
                "outputSpeech": build_correct_output_speech(statement_options),
                "card": build_correct_card_type(statement_options)}

    return build_response(response)


def continue_dialog():
    message = {"shouldEndSession": False, "directives": [{"type": "Dialog.Delegate"}]}
    return build_response(message)


# def continue_dialog_update_intent(intent, slots_to_update, session_attributes={}):
#     return build_response("temp", session_attributes)


def create_dialog_directive(directive_type, slots_to_update, intent_name, slot_to_elicit):
    slots = {}

    for slot_data in slots_to_update:
        slots[slot_data["slot_name"]] = {
            "name": slot_data["slot_name"],
            "value": slot_data["value"],
            "confirmationStatus": "NONE"
        }

    directives = [
        {
            "type": directive_type,
            "slotToElicit": slot_to_elicit,
            "updatedIntent": {
                "name": intent_name,
                "confirmationStatus": "NONE",
                "slots": slots
            }
        }
    ]

    return directives


def create_dialog_elicit_slot(response_options, intent_name, slot_to_elicit):
    slots_to_update = response_options.slots
    response = {
        "shouldEndSession": False,
        "outputSpeech": build_correct_output_speech(response_options),
        "directives": create_dialog_directive("Dialog.ElicitSlot",
                                              slots_to_update, intent_name,
                                              slot_to_elicit)
    }
    return build_response(response)


class ResponseOptions(object):
    def __init__(self):
        self.title = None
        self.body = None
        self.session_attributes = {}
        self.reprompt = None
        self.ssml = None
        self.slots = None

        self.images = None
        self.link_account_card = None

    def set_options(self, title=None, body=None, sess_attr=None, ssml=None, reprompt=None,
                    images=None, account_card=None, slots=None):
        self.title = title
        self.body = body
        if sess_attr is None:
            self.session_attributes = {}
        else:
            self.session_attributes = sess_attr
        self.reprompt = reprompt
        self.ssml = ssml

        self.images = images
        self.link_account_card = account_card
        self.slots = slots
