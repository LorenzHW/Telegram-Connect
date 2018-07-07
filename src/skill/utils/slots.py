class Slots(object):
    def __init__(self):
        self.first_name = {"slot_name": "first_name", "value": None}
        self.message = {"slot_name": "message", "value": None}

    def update_slot(self, slot):
        if slot['name'] == 'first_name':
            self._update_first_name(slot['value'])
        elif slot['name'] == 'message':
            self._update_message(slot['value'])

    def get_slots_in_list(self):
        return [self.first_name, self.message]

    def _update_first_name(self, value):
        self.first_name["value"] = value

    def _update_message(self, value):
        self.message["value"] = value
