import typing

if typing.TYPE_CHECKING:
    pass


class CanFulfillResponseCustom(object):
    deserialized_types = {
        'can_fulfill_intent': 'src.ask_sdk_custom.can_fulfill_intent_custom',
    }

    attribute_map = {
        'can_fulfill_intent': 'canFulfillIntent',
    }

    def __init__(self, can_fulfill_intent):
        self.can_fulfill_intent = can_fulfill_intent
