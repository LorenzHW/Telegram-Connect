from decimal import Decimal

from boto3.dynamodb.types import Binary


class State:
    def __init__(self, timezone, data=None):
        self._timezone = timezone
        self.new_session_count = Decimal(0)
        self.dc_id = Decimal(0)
        self.auth_key = None
        self.test_mode = None
        self.user_id = Decimal(0)
        self.is_bot = False
        self.peers = []

        if data:
            self._fill_state(data)

    def to_dict(self):
        return {
            "new_session_count": self.new_session_count,
            "dc_id": self.dc_id,
            "auth_key": self.auth_key,
            "test_mode": self.test_mode,
            "user_id": self.user_id,
            "is_bot": self.is_bot,
            "peers": self.peers
        }

    def _fill_state(self, data):
        self.new_session_count = data.get("new_session_count", Decimal(0))
        self.dc_id = data.get('dc_id', Decimal(0))
        self.auth_key = data.get('auth_key')
        if isinstance(self.auth_key, Binary):
            self.auth_key = self.auth_key.value
        self.test_mode = data.get('test_mode')
        self.user_id = data.get('user_id', Decimal(0))
        self.is_bot = data.get('is_bot', False)
        self.peers = data.get('peers', [])
