class DailyTelegramsAccount(object):
    """
    Holds data from the backend.
    """
    def __init__(self, id, phone_number, authorized):
        """
        Arguments:
            id {String} -- Id of the DailyTelegramsAccount in the backend.
            phone_number {String} -- Phone number of user.
            authorized {Boolean} -- Whether user is already authorized or not.
        """
        self.id = id
        self.phone_number = phone_number
        self.is_authorized = authorized


class Contact(object):
    """
    Holds data from the  backend. This is used for speed dial contacts, as well as contacts from
    the Telegram API.
    """
    def __init__(self, first_name, speed_dial_number=None, last_name=None, entity_id=None):
        """
        
        Arguments:
            first_name {String} -- First name of contact
            speed_dial_number {Int} -- Speed dial number of contact (default: {None})
            last_name {String} -- Last name of contact (default: {None})
            entity_id {String} -- ID from Telegram API. Needed for sending a Telegram (default: {None})        
        """
        self.first_name = first_name
        self.speed_dial_number = speed_dial_number
        self.last_name = last_name
        self.entity_id = entity_id


class Conversation(object):
    """
    Helper model to distinguish between group chats and dialogs. Used for creating the
    appropriate response when telegrams are read to the user.
    """
    def __init__(self, sender, telegrams, is_group, entity_id):
        """
        Arguments:
            sender {String} -- Can be either the name of a group name or the name of a contact
            telegrams {List} -- List of strings which contain the spoken telegrams.
            is_group {Boolean} -- Whether conversation is group chat or dialog
            entity_id {String} -- ID from Telegram API. Assigned to each individual chat.
        """
        self.sender = sender
        self.telegrams = telegrams
        self.is_group = is_group
        self.entity_id = entity_id
