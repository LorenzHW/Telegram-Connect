from typing import List, Tuple, Union, Coroutine, Any

from pyrogram import Client
from pyrogram.storage import Storage
from pyrogram.storage.sqlite_storage import get_input_peer
from pyrogram.types import Message

from secrets import API_ID, API_HASH
from skill.state_manager import StateManager


class DynamoDBStorage(Storage):

    def __init__(self, name: str, state_manager: StateManager):
        super().__init__(name)
        self.state_manager = state_manager
        self.state = state_manager.state

    async def open(self):
        print('DynamoDBStorage OPEN')
        pass

    async def save(self):
        print('DynamoDBStorage SAVE')
        self.state_manager.save_to_database()

    async def close(self):
        print('DynamoDBStorage CLOSE')

    async def delete(self):
        print('DynamoDBStorage DELETE')

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        """
        peers: id, access_hash, type, username, phone_number
        """
        print('DynamoDBStorage update_peers')
        peer_id_to_index = {p[0]: idx for idx, p in enumerate(self.state.peers)}

        for p1 in peers:
            p1 = list(p1)
            if p1[0] in peer_id_to_index:
                self.state.peers[peer_id_to_index[p1[0]]] = p1
                continue
            self.state.peers.append(p1)
        self.state_manager.save_to_database()

    async def get_peer_by_id(self, peer_id: int):
        print('DynamoDBStorage get_peer_by_id')
        r = list(filter(lambda p: p[0] == peer_id, self.state.peers))
        if not r:
            raise KeyError(f"ID not found: {peer_id}")
        r = r[0]
        return get_input_peer(*r[:3])

    async def get_peer_by_username(self, username: str):
        print('DynamoDBStorage get_peer_by_username')

    async def get_peer_by_phone_number(self, phone_number: str):
        print('DynamoDBStorage get_peer_by_phone_number')

    async def dc_id(self, value: int = object):
        print('DynamoDBStorage dc_id')
        if isinstance(value, int):
            self.state.dc_id = value
            self.state_manager.save_to_database()
        return self.state.dc_id

    async def test_mode(self, value: bool = object):
        print('DynamoDBStorage test_mode')
        if isinstance(value, bool):
            self.state.test_mode = value
            self.state_manager.save_to_database()
        return self.state.test_mode

    async def auth_key(self, value: bytes = object):
        print('DynamoDBStorage auth_key')
        if isinstance(value, bytes):
            self.state.auth_key = value
            self.state_manager.save_to_database()
        return self.state.auth_key

    async def date(self, value: int = object):
        print('DynamoDBStorage date')
        if isinstance(value, int):
            self.state.date = value
            self.state_manager.save_to_database()
        return self.state.date

    async def user_id(self, value: int = object):
        print('DynamoDBStorage user_id')
        if isinstance(value, int):
            self.state.user_id = value
            self.state_manager.save_to_database()
        return self.state.user_id

    async def is_bot(self, value: bool = object):
        print('DynamoDBStorage is_bot')
        if isinstance(value, bool):
            self.state.is_bot = value
            self.state_manager.save_to_database()
        return self.state.is_bot


class PyrogramManager:
    MEDIA_FILE_KEY = 'media_file_key'

    def __init__(self, state_manager: StateManager):
        self.client = Client(DynamoDBStorage('my_dynamo_db_storage', state_manager), API_ID, API_HASH)
        self._is_authorized = self.client.connect()


    @property
    def is_authorized(self):
        return self._is_authorized

    @is_authorized.setter
    def is_authorized(self, value):
        self._is_authorized = value

    def send_code(self, phone_number):
        print('PyrogramManager send_code')
        result = self.client.send_code(phone_number)
        return result.phone_code_hash

    def sign_in(self, phone_num, phone_code_hash, code):
        print('PyrogramManager sign_in')
        result = self.client.sign_in(phone_num, phone_code_hash, str(code))
        return result

    def get_unread_dialogs(self) -> List[dict]:
        all_dialogs = self.client.get_dialogs(limit=3)
        unread_dialogs = [dialog for dialog in all_dialogs if dialog.unread_messages_count > 0]
        data = []
        for dialog in unread_dialogs:
            messages = self.client.get_history(dialog.chat.id, dialog.unread_messages_count)
            data.append(
                {
                    "name": dialog.chat.first_name if dialog.chat.first_name else dialog.chat.title,
                    "telegrams": self._get_unread_telegrams(messages),
                    "is_group": True if dialog.chat.type in ['group', 'supergroup', 'channel'] else False,
                    "chat_id": dialog.chat.id
                }
            )
        return data

    def read_history(self, chat_id: Union[str, int]) -> Coroutine[Any, Any, bool]:
        return self.client.read_history(chat_id)

    def _get_unread_telegrams(self, messages: List[Message]) -> List[Tuple[str, str]]:
        messages.reverse()
        telegrams = [self._extract_data(m) for m in messages]
        return telegrams

    def _extract_data(self, m: Message) -> Tuple[str, str]:
        from_user = m.from_user.first_name if m.from_user else ''
        if m.media:
            return self.MEDIA_FILE_KEY, from_user
        if m.text:
            return m.text, from_user
        return 'Undetected file format.', from_user
