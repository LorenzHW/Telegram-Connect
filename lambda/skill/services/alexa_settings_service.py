import requests
from typing import Tuple


class AlexaSettingsService:
    def __init__(self, system, locale):
        self.api_endpoint = system.api_endpoint
        self.api_access_token = system.api_access_token
        self.device_id = system.device.device_id
        self.locale = locale

        self.timezone_endpoint = self.api_endpoint + "/v2/devices/{}/settings/System.timeZone"
        self.phone_number_endpoint = self.api_endpoint + "/v2/accounts/~current/settings/Profile.mobileNumber"

    def get_tz_database_name(self):
        url = self.timezone_endpoint.format(self.device_id)
        tz_database_name = self._execute_get_request(url)

        # If we don't have a string here, we have some kind of error response from the server
        if type(tz_database_name) != str:
            tz_database_name = "America/Los_Angeles"
            if self.locale == "de-DE":
                tz_database_name = "Europe/Vienna"
            elif self.locale == "en-GB":
                tz_database_name = "Europe/London"
            elif self.locale == "en-IN":
                tz_database_name = "Indian/Kerguelen"
            elif self.locale == "en-AU":
                tz_database_name = "Australia/Canberra"

        return tz_database_name

    def get_phone_number(self) -> Tuple[str, bool]:
        response = self._execute_get_request(self.phone_number_endpoint)
        is_success = False
        if 'countryCode' in response and 'phoneNumber' in response:
            is_success = True
            return response['countryCode'] + response['phoneNumber'], is_success
        elif 'code' in response:
            return response['code'], is_success
        return "", is_success

    def _execute_get_request(self, url):
        auth_string = "Bearer " + self.api_access_token
        headers = {'Authorization': auth_string}

        r = requests.get(url, headers=headers)
        return r.json()
