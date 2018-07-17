class DailyTelegramsAccount(object):
    def __init__(self, id, phone_number):
        self.id = id
        self.phone_number = phone_number


class Contact(object):
    def __init__(self, first_name, speed_dial_number=None, last_name=None):
        self.first_name = first_name
        self.speed_dial_number = speed_dial_number
        self.last_name = last_name


class Conversation(object):
    def __init__(self, sender, telegrams, is_group=False):
        self.sender = sender
        self.telegrams = telegrams
        self.is_group = is_group
