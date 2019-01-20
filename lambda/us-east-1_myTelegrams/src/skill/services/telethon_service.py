import requests

from src.skill.models.general_models import Contact, Conversation
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import BackendException, TelethonException


class TelethonService(object):
    """
    Communicates with my server.
    """
    contacts_url = 'https://www.lorenzhofmannw.com/telexa/api/contacts/'
    account_url = 'https://www.lorenzhofmannw.com/telexa/api/accounts/'
    telethon_code_request_url = 'https://www.lorenzhofmannw.com/telexa/api/telethon/authorization/'
    telethon_sign_in_url = 'https://www.lorenzhofmannw.com/telexa/api/telethon/authorization/?code={}&phone_code_hash={}'
    telethon_contacts_url = 'https://www.lorenzhofmannw.com/telexa/api/telethon/handler/?intent=SendIntent&slot_value={}'
    telethon_send_telegram_url = 'https://www.lorenzhofmannw.com/telexa/api/telethon/handler/?intent=SendIntent&entity_id={}&message={}'
    telethon_message_url = 'https://www.lorenzhofmannw.com/telexa/api/telethon/handler/?intent=MessageIntent&send_ack={}'

    def __init__(self):
        pass

    def send_code_request(self):
        r = self._execute_request(self.telethon_code_request_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            response = r.json()
            self._check_for_telethon_eception(response)

            phone_code_hash = str(response.get('phone_code_hash'))
            return phone_code_hash

    def sign_user_in(self, code, phone_code_hash):
        r = self._execute_request(self.telethon_sign_in_url.format(code, phone_code_hash))

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            response = r.json()
            self._check_for_telethon_eception(response)

            return True

    def check_telegrams(self):
        r = self._execute_request(self.telethon_message_url.format("False"))
        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            telegram_dialogs = r.json()
            self._check_for_telethon_eception(telegram_dialogs)
            if len(telegram_dialogs):
                return True
            else:
                return False

    def get_conversations(self, i18n):
        r = self._execute_request(self.telethon_message_url.format("True"))

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            telegram_dialogs = r.json()
            self._check_for_telethon_eception(telegram_dialogs)

            conversations = []
            for dialog in telegram_dialogs:
                if dialog.get("is_group"):
                    group_telegrams = []
                    for telegram_container in dialog.get("telegrams"):
                        sender = telegram_container[1]
                        telegram = telegram_container[0] + i18n.BREAK_150 \
                            if telegram_container[0] else i18n.MEDIA_FILE + i18n.BREAK_150

                        formatted_telegrams = i18n.GROUP_MESSAGE_INTRO.format(sender) + telegram
                        group_telegrams.append(formatted_telegrams)

                    conv = Conversation(dialog.get("name"), group_telegrams, True,
                                        dialog.get("entity_id"))
                else:
                    conv = Conversation(dialog.get("name"),
                                        [telegram_container[0] + i18n.BREAK_150 if
                                         telegram_container[0]
                                         else i18n.MEDIA_FILE + i18n.BREAK_150
                                         for telegram_container in dialog.get("telegrams")],
                                        False, dialog.get("entity_id"))
                conversations.append(conv)

            return conversations

    def get_potential_contacts(self, first_name):
        r = self._execute_request(self.telethon_contacts_url.format(first_name))

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            contacts_info = r.json()
            self._check_for_telethon_eception(contacts_info)

            potential_contacts = []
            for info in contacts_info:
                contact = Contact(info.get("name"), entity_id=info.get("id"))
                potential_contacts.append(contact)

            return potential_contacts

    def send_telegram(self, telethon_entity_id, message):
        r = self._execute_request(
            self.telethon_send_telegram_url.format(telethon_entity_id, message))

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            response = r.json()
            self._check_for_telethon_eception(response)

    def _check_for_telethon_eception(self, response):
        # Error messages come back as dict
        if isinstance(response, dict):
            if response.get("exception") and response.get("seconds"):
                # We got FloodWaitError --> User needs to wait for x seconds to use
                # Telegram API again.
                seconds = response.get("seconds")
                name = response.get("exception")
                raise TelethonException(response.get("message"), seconds=seconds, name=name)
            elif response.get("exception"):
                name = response.get("exception")
                raise TelethonException(response.get("message"), name=name)

    def _create_authorization_header(self):
        """
        Authorization header constructed as in docs:
        https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-5-testing-restricted-access
        :return: Dictionary with the header.
        """
        auth_string = "Bearer " + Constants.ACCESS_TOKEN
        headers = {'Authorization': auth_string}

        return headers

    def _execute_request(self, url):
        headers = self._create_authorization_header()

        r = requests.get(url, headers=headers)

        if r.ok:
            return r
        else:
            # some error
            print(r)
            return r.status_code
