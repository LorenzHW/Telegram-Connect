import typing

from ask_sdk_model import RequestEnvelope

if typing.TYPE_CHECKING:
    from typing import Optional
    from ask_sdk_model.session import Session
    from ask_sdk_model.request import Request
    from ask_sdk_model.context import Context


class RequestEnvelopeCustom(RequestEnvelope):
    deserialized_types = {
        'version': 'str',
        'session': 'ask_sdk_model.session.Session',
        'context': 'ask_sdk_model.context.Context',
        'request': 'src.ask_sdk_custom.ask_sdk_model_custom.request_custom.RequestCustom'
    }

    def __init__(self, version=None, session=None, context=None, request=None):
        # type: (Optional[str], Optional[Session], Optional[Context], Optional[Request]) -> None
        super().__init__(version, session, context, request)
