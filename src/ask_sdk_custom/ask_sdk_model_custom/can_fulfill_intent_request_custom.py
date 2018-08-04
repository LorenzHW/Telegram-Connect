import typing

from src.ask_sdk_custom.ask_sdk_model_custom.request_custom import RequestCustom

if typing.TYPE_CHECKING:
    from typing import Optional
    from datetime import datetime


class CanFulfillIntentRequestCustom(RequestCustom):
    def __init__(self, request_id=None, timestamp=None, locale=None):
        # type: (Optional[str], Optional[datetime], Optional[str]) -> None
        """An IntentRequest is an object that represents a request made to a skill based on what the user wants to do.

        :param request_id: Represents the unique identifier for the specific request.
        :type request_id: (optional) str
        :param timestamp: Provides the date and time when Alexa sent the request as an ISO 8601 formatted string. Used to verify the request when hosting your skill as a web service.
        :type timestamp: (optional) datetime
        :param locale: A string indicating the user’s locale. For example: en-US.
        :type locale: (optional) str
        :param dialog_state: Enumeration indicating the status of the multi-turn dialog. This property is included if the skill meets the requirements to use the Dialog directives. Note that COMPLETED is only possible when you use the Dialog.Delegate directive. If you use intent confirmation, dialogState is considered COMPLETED if the user denies the entire intent (for instance, by answering “no” when asked the confirmation prompt). Be sure to also check the confirmationStatus property on the Intent object before fulfilling the user’s request.
        :type dialog_state: (optional) ask_sdk_model.dialog_state.DialogState
        :param intent: An object that represents what the user wants.
        :type intent: (optional) ask_sdk_model.intent.Intent
        """
        self.__discriminator_value = "CanFulfillIntentRequestCustom"

        self.object_type = self.__discriminator_value
        super(CanFulfillIntentRequestCustom, self).__init__(object_type=self.__discriminator_value,
                                                            request_id=request_id,
                                                            timestamp=timestamp,
                                                            locale=locale)
