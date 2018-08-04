import typing

if typing.TYPE_CHECKING:
    pass


class CanFulfillSlotCustom(object):
    deserialized_types = {
        'can_understand': 'str',
        'can_fulfill': 'str',
    }

    attribute_map = {
        'can_understand': 'canUnderstand',
        'can_fulfill': 'canFulfill',
    }

    def __init__(self, can_understand=None, can_fulfill=None):
        self.can_understand = can_understand
        self.can_fulfill = can_fulfill
