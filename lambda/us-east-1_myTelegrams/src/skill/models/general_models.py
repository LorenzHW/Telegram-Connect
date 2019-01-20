class DailyTelegramsAccount(object):
    def __init__(self, id, phone_number, authorized, settings_id):
        self.id = id
        self.phone_number = phone_number
        self.is_authorized = authorized
        self.settings_id = settings_id


class Contact(object):
    def __init__(self, first_name, speed_dial_number=None, last_name=None, entity_id=None):
        self.first_name = first_name
        self.speed_dial_number = speed_dial_number
        self.last_name = last_name
        self.entity_id = entity_id


class Conversation(object):
    def __init__(self, sender, telegrams, is_group, entity_id):
        self.sender = sender
        self.telegrams = telegrams
        self.is_group = is_group
        self.entity_id = entity_id

class Settings(object):
    def __init__(self, settings_id, non_verbose_mode):
        self.id = settings_id
        self.non_verbose_mode = non_verbose_mode

    def to_dict(self):
        result = {}
        result['non_verbose_mode'] = self.non_verbose_mode
        return result