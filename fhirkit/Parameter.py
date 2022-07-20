try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from typing import Any, List, Optional, Union
from pydantic import (
    Field,
    HttpUrl,
    StrictInt,
    StrictStr,
    StrictBool,
    validator,
)
from fhirkit.choice_type import deterimine_choice_type
from fhirkit.Resource import Resource
from fhirkit.primitive_datatypes import Code
from fhirkit.elements import BackboneElement, CodeableConcept, Coding


class AbstractParameter(BackboneElement):
    name: str


class ValueParameter(AbstractParameter):
    valueBoolean: Optional[bool] = Field(None, exclude=True)
    value: Union[
        StrictBool, StrictStr, Code, Coding, CodeableConcept, HttpUrl, StrictInt
    ] = None

    @validator("value", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)

    def __str__(self) -> str:
        return f"{self.name}:{self.value}"


class ResourceParameter(AbstractParameter):
    resource: Optional[Resource]


class MultiPartParameter(AbstractParameter):
    part: List[ValueParameter]

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            for param in self.part:
                if param.name == __name:
                    return param.value
            raise

    def __str__(self) -> str:
        return "\n\tpart: \n" + "\n\t".join(" " + str(p) for p in self.part)


class Parameters(Resource):
    resourceType: Literal["Parameters"] = Field("Parameters", const=True)
    parameter: List[Union[ValueParameter, ResourceParameter, MultiPartParameter]]

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            for param in self.parameter:
                if param.name == __name:
                    return param.value
            raise

    def __str__(self) -> str:
        return "Parameters: \n" + "\n".join(" " + str(p) for p in self.parameter)
