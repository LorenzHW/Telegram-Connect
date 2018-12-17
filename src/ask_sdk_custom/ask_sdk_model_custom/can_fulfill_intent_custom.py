import typing

if typing.TYPE_CHECKING:
    pass


class CanFulfillIntentCustom(object):
    """
    # TODO: this will probably be deprecated.  I used the beta version of the SDK. The next time
    # TODO: I touch the code, this should be available in the SDK. Used for CanFulFill
    """
    deserialized_types = {
        'can_fulfill': 'str',
        'slots': 'dict(str, src.ask_sdk_custom.ask_sdk_model_custom.can_fulfill_slot_custom.CanFulfillSlotCustom)',
    }

    attribute_map = {
        'can_fulfill': 'canFulfill',
        'slots': 'slots',
    }

    def __init__(self, can_fulfill=None, slots=None):
        self.can_fulfill = can_fulfill # YES, NO, or MAYBE
        self.slots = slots
