import typing

if typing.TYPE_CHECKING:
    pass


class CanFulfillSlotCustom(object):
    """
    # TODO: this will probably be deprecated.  I used the beta version of the SDK. The next time
    # TODO: I touch the code, this should be available in the SDK. Used for CanFulFill
    """
    deserialized_types = {
        'can_understand': 'str',
        'can_fulfill': 'str',
    }

    attribute_map = {
        'can_understand': 'canUnderstand',
        'can_fulfill': 'canFulfill',
    }

    def __init__(self, can_understand=None, can_fulfill=None):
        self.can_understand = can_understand  # YES, NO, or MAYBE
        self.can_fulfill = can_fulfill  # YES, NO (entity resolution)
