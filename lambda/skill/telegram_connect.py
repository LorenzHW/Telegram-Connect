# -*- coding: utf-8 -*-
import ask_sdk_core.utils as ask_utils
import ask_sdk_dynamodb
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from skill.helper_functions import set_explore_sess_attr, ExploreIntents
from skill.i18n.util import get_i18n
from skill.intents.general_intents import HelpIntentHandler, CancelOrStopIntentHandler, SessionEndedRequestHandler, \
    IntentReflectorHandler, CatchAllExceptionHandler, FallbackIntentHandler
from skill.intents.learn_more_intent import LearnMoreIntentHandler
from skill.intents.message_intent import MessageIntentHandler
from skill.intents.no_intent import NoIntentHandler
from skill.intents.setup_intent import SetupIntentHandler
from skill.intents.yes_intent import YesIntentHandler
from skill.interceptors import StateRequestInterceptor, LoggingRequestInterceptor, CardResponseInterceptor

import logging

from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.state_manager import StateManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = get_i18n(handler_input.request_envelope.request.locale, sess_attrs.get("tz_database_name"))
        pyrogram_manager = PyrogramManager(StateManager(handler_input))

        if not pyrogram_manager.is_authorized:
            set_explore_sess_attr(sess_attrs, ExploreIntents.EXPLORE_SETUP_INTENT)
            return handler_input.response_builder.speak(i18n.NEW_SETUP).ask(i18n.FALLBACK).response

        new_telegrams = pyrogram_manager.get_unread_telegrams()
        if new_telegrams:
            speech = i18n.WELCOME_BACK + ' ' + i18n.NEW_TELEGRAMS
            set_explore_sess_attr(sess_attrs, ExploreIntents.EXPLORE_MESSAGE_INTENT)
            sess_attrs['new_telegrams'] = new_telegrams
            return handler_input.response_builder.speak(speech).ask(i18n.FALLBACK).response

        speech = i18n.WELCOME_BACK + ' ' + i18n.NO_NEW_TELEGRAMS + ' ' + i18n.get_random_anyting_else()
        return handler_input.response_builder.speak(speech).ask(i18n.FALLBACK).response


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = StandardSkillBuilder(table_name='TelegramConnectSkill', auto_create_table=False,
                          partition_keygen=ask_sdk_dynamodb.partition_keygen.user_id_partition_keygen)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(SetupIntentHandler())
sb.add_request_handler(MessageIntentHandler())
sb.add_request_handler(LearnMoreIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_request_interceptor(StateRequestInterceptor())

sb.add_global_response_interceptor(CardResponseInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
