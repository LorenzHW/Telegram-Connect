import json
import typing

from ask_sdk_core.skill import Skill
from ask_sdk_core.skill_builder import SkillBuilder

from src.ask_sdk_custom.ask_sdk_model_custom.request_envelope_custom import RequestEnvelopeCustom

if typing.TYPE_CHECKING:
    from typing import Callable, TypeVar, Dict

    T = TypeVar('T')


class SkillBuilderCustom(SkillBuilder):
    def __init__(self):
        super().__init__()

    def lambda_handler(self):
        # type: () -> Callable[[RequestEnvelopeCustom, T], Dict[str, T]]
        """Create a handler function that can be used as handler in
        AWS Lambda console.

        The lambda handler provides a handler function, that acts as
        an entry point to the AWS Lambda console. Users can set the
        lambda_handler output to a variable and set the variable as
        AWS Lambda Handler on the console.

        :return: Handler function to tag on AWS Lambda console.
        """

        def wrapper(event, context):
            # type: (RequestEnvelopeCustom, T) -> Dict[str, T]
            skill = Skill(skill_configuration=self.skill_configuration)
            request_envelope = skill.serializer.deserialize(
                payload=json.dumps(event), obj_type=RequestEnvelopeCustom)
            response_envelope = skill.invoke(
                request_envelope=request_envelope, context=context)
            return skill.serializer.serialize(response_envelope)

        return wrapper
