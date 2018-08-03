from src.skill.i18n.language_model import LanguageModel


def respond_to_http_error_code(handler_input, http_error_code):
    i18n = LanguageModel(handler_input.request_envelope.request.locale)
    sess_attrs = handler_input.attributes_manager.session_attributes

    if http_error_code == 401:
        # Unauthorized: Happens when user enables alexa skill with valid account
        # then deletes account on my webserver and uses skill again
        speech_text = i18n.ACCOUNT_LINKING_REQUIRED
        sess_attrs["LINK_ACCOUNT_CARD"] = True
    elif 500 <= http_error_code < 600:
        speech_text = i18n.SERVER_ERROR
    else:
        speech_text = i18n.BACKEND_EXCEPTION

    handler_input.response_builder.speak(speech_text).set_should_end_session(True)
    return handler_input.response_builder.response


def handle_telethon_error_response(error, handler_input):
    # speech_text = error.get("name")

    handler_input.response_builder.speak("some telethon error") \
        .set_should_end_session(True)
    return handler_input


class BackendException(Exception):
    def __init__(self, message):
        super(BackendException, self).__init__(message)


class TelethonException(Exception):
    def __init__(self, message, **kwargs):
        self.seconds = kwargs.get("seconds")
        self.name = kwargs.get("name")
        super(TelethonException, self).__init__(message)
