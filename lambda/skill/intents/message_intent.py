from typing import List, Tuple

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from skill.i18n.util import get_i18n
from skill.pyrogram.pyrogram_manager import PyrogramManager
from skill.state_manager import StateManager


class MessageIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if is_intent_name("MessageIntent")(handler_input):
            return True

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        self.i18n = get_i18n(handler_input)
        pyrogram_manager = PyrogramManager(StateManager(handler_input))

        if not pyrogram_manager.get_is_authorized():
            return handler_input.response_builder.speak(self.i18n.NOT_AUTHORIZED).set_should_end_session(True).response

        if 'unread_dialogs' not in sess_attrs:
            unread_dialogs = pyrogram_manager.get_unread_dialogs()
            sess_attrs['unread_dialogs'] = unread_dialogs
            if not unread_dialogs:
                speech = self.i18n.NO_NEW_TELEGRAMS + ' ' + self.i18n.get_random_goodbye()
                return handler_input.response_builder.speak(speech).response

        unread_dialogs_index = sess_attrs.get('unread_dialog_index', 0)
        unread_dialogs = sess_attrs.get('unread_dialogs', [])

        speech_text = ''
        if unread_dialogs_index == 0:
            first_names = self.get_first_names(unread_dialogs)
            speech_text += self.i18n.NEW_TELEGRAMS_FROM.format(first_names)

        dialog = unread_dialogs[unread_dialogs_index]
        pyrogram_manager.read_history(dialog['chat_id'])
        speech_text += self.construct_output_speech_for_dialog(dialog)

        if unread_dialogs_index == len(unread_dialogs) - 1:
            speech_text += self.i18n.BREAK_2000 + ' ' + self.i18n.NO_MORE_TELEGRAMS
            return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

        speech_text += self.i18n.BREAK_2000 + ' ' + self.i18n.NEXT_TELEGRAMS
        sess_attrs['unread_dialog_index'] = unread_dialogs_index + 1
        return handler_input.response_builder.speak(speech_text).ask(self.i18n.FALLBACK).response

    def get_first_names(self, unread_dialogs: List[dict]) -> str:
        if len(unread_dialogs) == 1:
            return unread_dialogs[0]['name'] + self.i18n.BREAK_200

        # Don't loop over last, because we add an 'and' for the voice output
        names = [telegram['name'] for telegram in unread_dialogs[:-1]]
        first_names = ", ".join(names) + self.i18n.BREAK_200
        first_names += ' ' + self.i18n.AND + ' ' + unread_dialogs[-1]['name'] + self.i18n.BREAK_200
        # Constructs a string like: "Tom, Paul, and Julia"
        return first_names

    def construct_output_speech_for_dialog(self, dialog: dict):
        speech_text = self.i18n.PERSONAL_DIALOG_INTRO.format(dialog['name'])
        if dialog['is_group']:
            speech_text = self.i18n.GROUP_DIALOG_INTRO.format(dialog['name']) + ': '
            spoken_telegrams = self.construct_spoken_telegrams(dialog['telegrams'], True)
            speech_text += (' ' + self.i18n.BREAK_350).join(spoken_telegrams)
            return speech_text

        spoken_telegrams = self.construct_spoken_telegrams(dialog['telegrams'], False)
        if dialog['telegrams'][0][0] == PyrogramManager.MEDIA_FILE_KEY:
            speech_text = ''

        speech_text += (' ' + self.i18n.BREAK_350).join(spoken_telegrams)
        return speech_text

    def construct_spoken_telegrams(self, telegrams: List[Tuple[str, str]], is_group: bool):
        spoken_telegrams = []
        for telegram, from_user in telegrams:
            to_append = telegram
            if is_group:
                to_append = self.i18n.PERSONAL_DIALOG_INTRO.format(from_user) + self.i18n.BREAK_200 + telegram
            if telegram == PyrogramManager.MEDIA_FILE_KEY:
                to_append = self.i18n.MEDIA_FILE_RECEIVED.format(from_user)
            spoken_telegrams.append(to_append)
        return spoken_telegrams
