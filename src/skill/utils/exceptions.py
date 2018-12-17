from src.skill.i18n.language_model import LanguageModel


def respond_to_http_error_code(handler_input, http_error_code):
    """
    Builds the appropiate response for the user to hear based on the HTTP error code
    we retrive from the backend.
    
    Arguments:
        handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
        http_error_code {Integer} -- Error code from the backend.
    
    Returns:
        [ask_sdk_model.response.Response] -- Response object
    """
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
    """
    Give appropiate response to user based Telegram's error information.
    
    Arguments:
        error {String} -- Error name from Telethon wrapper (see GitHub repo of Telethon)
        handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.

    Returns:
        handler_input {ask_sdk_core.handler_input.HandlerInput} -- Provided by Amazon's SDK.
    """

    i18n = LanguageModel(handler_input.request_envelope.request.locale)
    error_name = error.name

    if error_name == "SessionPasswordNeededError":
        speech_text = i18n.TWO_STEPS_VERIFICATION_ERROR
    elif error_name == "FloodWaitError":
        h, m = calculate_hours_and_minutes_from_seconds(error.seconds)
        speech_text = i18n.FLOODWAIT_ERROR.format(h, m)
    elif error_name == "PhoneNumberUnoccupiedError":
        speech_text = i18n.INVALID_PHONE
    elif error_name == "PhoneNumberInvalidError":
        speech_text = i18n.INVALID_PHONE
    elif error_name == "PhoneCodeExpiredError":
        speech_text = i18n.CODE_EXPIRED
    elif error_name == "PhoneCodeInvalidError":
        speech_text = i18n.CODE_INVALID
    elif error_name == "AuthKeyUnregisteredError":
        speech_text = i18n.SERVER_ERROR
    elif error_name == "ChatAdminRequiredError":
        speech_text = i18n.CHAT_ADMIN_REQUIRED_ERROR

    handler_input.response_builder.speak(speech_text) \
        .set_should_end_session(True)
    return handler_input


def calculate_hours_and_minutes_from_seconds(seconds):
    """
    Helper method.
    TODO: should be in utils.py
    
    Arguments:
        seconds {Int} -- Number of seconds
    
    Returns:
        [Tuple] -- Tuple with hours and minutes.
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return h, m


class BackendException(Exception):
    """
    Raised if backend returns HTTP error code.
    
    Arguments:
        Exception {[type]} -- [description]
    """
    def __init__(self, message):
        super(BackendException, self).__init__(message)


class TelethonException(Exception):
    """
    Raised if Telegram's API returns an error.
    
    Arguments:
        Exception {[type]} -- [description]
    """
    
    def __init__(self, message, **kwargs):
        super(TelethonException, self).__init__(message)
        self.seconds = kwargs.get("seconds")
        self.name = kwargs.get("name")
