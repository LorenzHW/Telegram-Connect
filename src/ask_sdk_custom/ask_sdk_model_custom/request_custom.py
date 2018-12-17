import typing

from ask_sdk_model import Request

if typing.TYPE_CHECKING:
    from typing import Optional
    from datetime import datetime


class RequestCustom(Request):
    """
    # TODO: this will probably be deprecated.  I used the beta version of the SDK. The next time
    # TODO: I touch the code, this should be available in the SDK. Used for CanFulFill
    """
    discriminator_value_class_map = {
        'AudioPlayer.PlaybackStopped': 'ask_sdk_model.interfaces.audioplayer.playback_stopped_request.PlaybackStoppedRequest',
        'AudioPlayer.PlaybackFinished': 'ask_sdk_model.interfaces.audioplayer.playback_finished_request.PlaybackFinishedRequest',
        'AlexaSkillEvent.SkillEnabled': 'ask_sdk_model.events.skillevents.skill_enabled_request.SkillEnabledRequest',
        'AlexaHouseholdListEvent.ListUpdated': 'ask_sdk_model.services.list_management.list_updated_event_request.ListUpdatedEventRequest',
        'PlaybackController.PreviousCommandIssued': 'ask_sdk_model.interfaces.playbackcontroller.previous_command_issued_request.PreviousCommandIssuedRequest',
        'AlexaSkillEvent.SkillDisabled': 'ask_sdk_model.events.skillevents.skill_disabled_request.SkillDisabledRequest',
        'Display.ElementSelected': 'ask_sdk_model.interfaces.display.element_selected_request.ElementSelectedRequest',
        'AlexaHouseholdListEvent.ItemsUpdated': 'ask_sdk_model.services.list_management.list_items_updated_event_request.ListItemsUpdatedEventRequest',
        'AlexaSkillEvent.SkillPermissionChanged': 'ask_sdk_model.events.skillevents.permission_changed_request.PermissionChangedRequest',
        'AlexaHouseholdListEvent.ItemsCreated': 'ask_sdk_model.services.list_management.list_items_created_event_request.ListItemsCreatedEventRequest',
        'AlexaSkillEvent.SkillAccountLinked': 'ask_sdk_model.events.skillevents.account_linked_request.AccountLinkedRequest',
        'SessionEndedRequest': 'ask_sdk_model.session_ended_request.SessionEndedRequest',
        'AlexaHouseholdListEvent.ListCreated': 'ask_sdk_model.services.list_management.list_created_event_request.ListCreatedEventRequest',
        'AudioPlayer.PlaybackStarted': 'ask_sdk_model.interfaces.audioplayer.playback_started_request.PlaybackStartedRequest',
        'IntentRequest': 'ask_sdk_model.intent_request.IntentRequest',
        'CanFulfillIntentRequest': 'src.ask_sdk_custom.ask_sdk_model_custom.can_fulfill_intent_request_custom.CanFulfillIntentRequestCustom',
        'AudioPlayer.PlaybackNearlyFinished': 'ask_sdk_model.interfaces.audioplayer.playback_nearly_finished_request.PlaybackNearlyFinishedRequest',
        'AlexaHouseholdListEvent.ItemsDeleted': 'ask_sdk_model.services.list_management.list_items_deleted_event_request.ListItemsDeletedEventRequest',
        'Connections.Response': 'ask_sdk_model.interfaces.connections.connections_response.ConnectionsResponse',
        'Messaging.MessageReceived': 'ask_sdk_model.interfaces.messaging.message_received_request.MessageReceivedRequest',
        'AudioPlayer.PlaybackFailed': 'ask_sdk_model.interfaces.audioplayer.playback_failed_request.PlaybackFailedRequest',
        'Connections.Request': 'ask_sdk_model.interfaces.connections.connections_request.ConnectionsRequest',
        'System.ExceptionEncountered': 'ask_sdk_model.interfaces.system.exception_encountered_request.ExceptionEncounteredRequest',
        'AlexaSkillEvent.SkillPermissionAccepted': 'ask_sdk_model.events.skillevents.permission_accepted_request.PermissionAcceptedRequest',
        'AlexaHouseholdListEvent.ListDeleted': 'ask_sdk_model.services.list_management.list_deleted_event_request.ListDeletedEventRequest',
        'GameEngine.InputHandlerEvent': 'ask_sdk_model.interfaces.game_engine.input_handler_event_request.InputHandlerEventRequest',
        'PlaybackController.NextCommandIssued': 'ask_sdk_model.interfaces.playbackcontroller.next_command_issued_request.NextCommandIssuedRequest',
        'PlaybackController.PauseCommandIssued': 'ask_sdk_model.interfaces.playbackcontroller.pause_command_issued_request.PauseCommandIssuedRequest',
        'PlaybackController.PlayCommandIssued': 'ask_sdk_model.interfaces.playbackcontroller.play_command_issued_request.PlayCommandIssuedRequest',
        'LaunchRequest': 'ask_sdk_model.launch_request.LaunchRequest'
    }

    def __init__(self, object_type=None, request_id=None, timestamp=None, locale=None):
        # type: (Optional[str], Optional[str], Optional[datetime], Optional[str]) -> None
        super().__init__(object_type, request_id, timestamp, locale)
