import requests

from src.skill.models.general_models import Contact, Conversation
from src.skill.utils.constants import Constants
from src.skill.utils.utils import BackendException


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
    telethon_message_url = 'https://www.lorenzhofmannw.com/telexa/api/telethon/handler/?intent=MessageIntent'

    def __init__(self):
        pass

    def send_code_request(self):
        r = self.execute_request(self.telethon_code_request_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            response = r.json()
            phone_code_hash = str(response['phone_code_hash'])

            return phone_code_hash

    def sign_user_in(self, code, phone_code_hash):
        r = self.execute_request(self.telethon_sign_in_url.format(code, phone_code_hash))

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            response = r.json()
            # TODO: Some error handling in backend
            return True

    def check_telegrams(self):
        return True

    def get_conversations(self, i18n):
        r = self.execute_request(self.telethon_message_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            telegram_dialogs = r.json()
            conversations = []

            for dialog in telegram_dialogs:
                if dialog.get("is_group"):
                    group_telegrams = [i18n.GROUP_MESSAGE_INTO.format(telegram[1]) + telegram[0] for
                                       telegram in dialog.get("telegrams")]
                    conv = Conversation(dialog.get("name"), group_telegrams, True)
                else:
                    conv = Conversation(dialog.get("name"),
                                        [telegram[0] for telegram in dialog.get("telegrams")])
                conversations.append(conv)

            return conversations

        conversations = []

        conversations.append(Conversation("Tom", ["Hey man how is it going? <break time='100ms'/>",
                                                  "I am chillin here <break time='100ms'/>",
                                                  "This is the last message <break time='350ms'/>"]))  # longer break here
        conversations.append(
            Conversation("Tennis and Golf",
                         [
                             "Rainer wrote: Rafa is awesome <break time='100ms'/> He is literally the greated player on sand that ever existed <break time='200ms'/>",
                             "Thomas wrote: Definitely true <break time='350ms'/>"], True))
        conversations.append(Conversation("Sophia", ["Yo dude <break time='350ms'/>"]))
        conversations.append(Conversation("Some Bot", ["Yo dude <break time='350ms'/>"]))

        return conversations

    def get_potential_contacts(self, first_name):
        r = self.execute_request(self.telethon_contacts_url.format(first_name))

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            contacts_info = r.json()
            potential_contacts = []

            for info in contacts_info:
                contact = Contact(info.get("name"), telegram_id=info.get("id"))
                potential_contacts.append(contact)

            return potential_contacts

    def create_authorization_header(self):
        """
        Authorization header constructed as in docs:
        https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-5-testing-restricted-access
        :return: Dictionary with the header.
        """
        auth_string = "Bearer " + Constants.ACCESS_TOKEN
        headers = {'Authorization': auth_string}

        return headers

    def execute_request(self, url):
        headers = self.create_authorization_header()

        r = requests.get(url, headers=headers)

        if r.ok:
            return r
        else:
            # some error
            print(r)
            return r.status_code
