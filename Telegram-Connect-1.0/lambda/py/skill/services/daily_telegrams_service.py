import requests

from skill.models.general_models import DailyTelegramsAccount, Settings
from skill.utils.constants import Constants
from skill.utils.exceptions import BackendException


class DailyTelegramsService(object):
    """
    Communicates with my server.
    """
    contacts_url = 'https://www.lorenzhofmannw.com/telexa/api/contacts/'
    account_url = 'https://www.lorenzhofmannw.com/telexa/api/accounts/'
    settings_url = 'https://www.lorenzhofmannw.com/telexa/api/settings/'

    def __init__(self):
        pass

    def get_contacts(self):
        r = self._execute_get_request(self.contacts_url)
        if isinstance(r, int):
            raise BackendException(r)

        return r.json()

    def get_daily_telegrams_account(self):
        """
        We make here an call to a ListMixin. That is why we retrieve a list of users. However,
        this list contains only the authorized user.
        :return: DailyTelegramsAccount
        """
        r = self._execute_get_request(self.account_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            account_information = r.json()

            # Telephon API (or DynamoService?) expects an string. So lets cast it to a string.
            account_id = str(account_information[0].get("id"))
            phone_number = account_information[0].get("phone_number")
            is_authorized = account_information[0].get("is_authorized")
            settings_id = account_information[0].get("settings")
            daily_telegrams_account = DailyTelegramsAccount(
                account_id, phone_number, is_authorized, settings_id)

            return daily_telegrams_account

    def get_firstname_for_speed_dial_number(self, speed_dial_number):
        contacts = self.get_contacts()

        for contact_info in contacts:
            if contact_info['speed_dial_number'] == int(speed_dial_number):
                first_name = contact_info['first_name']
                return first_name

    def create_settings(self):
        r = self._execute_post_request(self.settings_url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            settings_information = r.json()
            return settings_information.get('id')

    def update_settings(self, settings_object):
        url = self.settings_url + str(settings_object.id) + '/'
        r = self._execute_put_request(url, data=settings_object.to_dict())

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            settings_information = r.json()
            settings_object.non_verbose_mode = settings_information.get('non_verbose_mode')
            return  settings_object

    def get_settings(self, id):
        url = self.settings_url + str(id) + '/'
        r = self._execute_get_request(url)

        if isinstance(r, int):
            # we got some http error status code
            raise BackendException(r)
        else:
            settings_information = r.json()
            return Settings(id, settings_information.get('non_verbose_mode'))


    def _create_authorization_header(self):
        """
        Authorization header constructed as in docs:
        https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-5-testing-restricted-access
        :return: Dictionary with the header.
        """
        auth_string = "Bearer " + Constants.ACCESS_TOKEN
        headers = {'Authorization': auth_string}

        return headers

    def _execute_get_request(self, url):
        headers = self._create_authorization_header()

        r = requests.get(url, headers=headers)

        if r.ok:
            return r
        else:
            # some error
            print(r)
            return r.status_code


    def _execute_post_request(self, url):
        headers = self._create_authorization_header()

        r = requests.post(url, headers=headers)

        if r.ok:
            return r
        else:
            # some error
            print(r)
            return r.status_code

    def _execute_put_request(self, url, data):
        headers = self._create_authorization_header()

        r = requests.put(url, headers=headers, data=data)

        if r.ok:
            return r
        else:
            # some error
            print(r)
            return r.status_code


    