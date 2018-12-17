import requests

from src.skill.models.general_models import DailyTelegramsAccount
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import BackendException


class DailyTelegramsService(object):
    """
    Communicates with the backend. This service is used to get information that is stored
    in my database and does not relate to Telegrams API.
    """
    contacts_url = 'https://www.lorenzhofmannw.com/telexa/api/contacts/'
    account_url = 'https://www.lorenzhofmannw.com/telexa/api/accounts/'

    def __init__(self):
        pass

    def get_contacts(self):
        """
        Gets all speed dial contacts the user has created.
        TODO: private method?
        
        Raises:
            BackendException -- [description]
        
        Returns:
            [type] -- [description]
        """

        r = self._execute_request(self.contacts_url)
        if isinstance(r, int):
            raise BackendException(r)

        return r.json()

    def get_daily_telegrams_account(self):
        """
        Gets info about the daily telegrams account from the backend. Due to account linking
        no further information is necessary for the backend. Backend logic handles which account
        to retrieve. Access Token is sent to backend. Hence, backend knows which account to get.

        Raises:
            BackendException -- [description]
        
        Returns:
            [src.skill.models.general_models.DailyTelegramsAccount] -- Account with info from the backend.
        """

        # We make here an call to a ListMixin. That is why we retrieve a list of users. However,
        # this list contains only the logged in user (due to account linking).
        r = self._execute_request(self.account_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            account_information = r.json()

            # Telephon API (or DynamoService?) expects an string. So lets cast it to a string.
            account_id = str(account_information[0].get("id"))
            phone_number = account_information[0].get("phone_number")
            is_authorized = account_information[0].get("is_authorized")
            daily_telegrams_account = DailyTelegramsAccount(account_id, phone_number, is_authorized)

            return daily_telegrams_account

    def get_firstname_for_speed_dial_number(self, speed_dial_number):
        """
        Compares the speed dial number from the user to the actual contacts that
        the user created.
        
        Arguments:
            speed_dial_number {String} -- The number the user said to Alexa
        
        Returns:
            [String] -- First name of the speed dial contact
        """
        contacts = self.get_contacts()

        for contact_info in contacts:
            if contact_info['speed_dial_number'] == int(speed_dial_number):
                first_name = contact_info['first_name']
                return first_name

    def _create_authorization_header(self):
        """
        Sets headers in HTTP request
        """

        # Authorization header constructed as in docs:
        # https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-5-testing-restricted-access
        auth_string = "Bearer " + Constants.ACCESS_TOKEN
        headers = {'Authorization': auth_string}

        return headers

    def _execute_request(self, url):
        #TODO: Refactor. Create abstract Service with methods _create_authorization_header
        #TODO: and _exceute_request. Same code in other service.
        """
        Executes HTTP requests

        Arguments:
            url {String} -- URLS to my backend
        
        Returns:
            [type] -- [description]
        """
        headers = self._create_authorization_header()

        r = requests.get(url, headers=headers)

        if r.ok:
            return r
        else:
            # some error
            print(r)
            return r.status_code
