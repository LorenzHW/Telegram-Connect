import traceback

from ask_sdk_runtime.dispatch_components import AbstractExceptionHandler

from skill.i18n.util import get_i18n


def print_traceback(exception: Exception):
    print("ENCOUNTERED FOLLOWING EXCEPTION:")
    print("PRINTING: TRACEBACK: ")
    print(traceback.format_exc())
    print(exception)
    print("PRINTING EXCEPTION ARGS:")
    for idx, arg in enumerate(exception.args):
        print("Arg number {}: {}".format(idx + 1, arg))


class NoSuccessRetrievingPhonenumberException(Exception):
    def __init__(self, *args):
        super(NoSuccessRetrievingPhonenumberException, self).__init__(*args)


class CatchNoSuccessRetrievingPhonenumberExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        if isinstance(exception, NoSuccessRetrievingPhonenumberException):
            return True
        return False

    def handle(self, handler_input, exception):
        rb = handler_input.response_builder
        i18n = get_i18n(handler_input)
        print("CATCH EXCEPTION")
        sess_attrs = handler_input.attributes_manager.session_attributes
        sess_attrs.clear()
        speech = i18n.EXCEPTION_RETRIEVING_PHONE_NUM
        print_traceback(exception)

        rb.speak(speech).set_should_end_session(True)
        return rb.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        print_traceback(exception)
        rb = handler_input.response_builder
        i18n = get_i18n(handler_input)

        sess_attrs = handler_input.attributes_manager.session_attributes
        sess_attrs.clear()

        speech = i18n.EXCEPTION

        rb.speak(speech).set_should_end_session(True)
        return rb.response
