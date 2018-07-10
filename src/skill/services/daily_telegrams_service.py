import requests

from src.skill.models.general_models import DailyTelegramsAccount, Contact
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import BackendException


class DailyTelegramsService(object):
    """
    Communicates with my server.
    """
    contacts_url = 'https://www.lorenzhofmannw.com/telexa/api/contacts/'
    account_url = 'https://www.lorenzhofmannw.com/telexa/api/accounts/'

    def __init__(self):
        pass

    def get_contacts(self):
        r = self.execute_request(self.contacts_url)
        if isinstance(r, int):
            raise BackendException(r)

        return r.json()

    def get_daily_telegrams_account(self):
        """
        We make here an call to a ListMixin. That is why we retrieve a list of users. However,
        this list contains only the authorized user.
        :return: DailyTelegramsAccount
        """
        r = self.execute_request(self.account_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            account_information = r.json()

            # Telephon API (or DynamoService?) expects an string. So lets cast it to a string.
            account_id = str(account_information[0]['id'])
            account_phone_number = account_information[0]['phone_number']
            daily_telegrams_account = DailyTelegramsAccount(account_id, account_phone_number)

            return daily_telegrams_account

    def get_contact_for_speed_dial_number(self, speed_dial_number):
        contacts = self.get_contacts()

        for contact_info in contacts:
            if contact_info['speed_dial_number'] == int(speed_dial_number):
                first_name = contact_info['first_name']
                last_name = contact_info['last_name']
                return Contact(first_name, speed_dial_number, last_name)

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
