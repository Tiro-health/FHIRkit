from typing import Any, ClassVar, List, Optional, Set, Union
from pydantic import (
    Field,
    HttpUrl,
    StrictInt,
    StrictStr,
    StrictBool,
    validator,
)
from fhirkit.ChoiceTypeMixin import ChoiceTypeMixinBase, validate_choice_types
from fhirkit.Resource import Resource
from fhirkit.data_types import Code
from fhirkit.elements import BackboneElement, CodeableConcept, Coding


class ParameterValueChoiceTypeMixin(ChoiceTypeMixinBase):
    _choice_type_fields: ClassVar[Set[str]] = [
        "valueBoolean",
        "valueString",
        "valueCode",
        "valueCoding",
        "valueCodeableConcept",
        "valueUri",
        "valueInteger",
    ]
    _polymorphic_field: ClassVar[Set[str]] = "value"
    valueBoolean: Optional[StrictBool] = Field(None)
    valueString: Optional[StrictStr] = Field(None)
    valueCode: Optional[Code] = Field(None)
    valueCoding: Optional[Coding] = Field(None)
    valueCodeableConcept: Optional[CodeableConcept] = Field(None)
    valueUri: Optional[HttpUrl] = Field(None)
    valueInteger: Optional[StrictInt] = Field(None)
    value: Union[
        StrictBool, StrictStr, Code, Coding, CodeableConcept, HttpUrl, StrictInt
    ] = Field(None, exclude=True)

    validate_value = validator("value", pre=True, always=True, allow_reuse=True)(
        validate_choice_types
    )


class AbstractParameter(BackboneElement):
    name: str


class ValueParameter(
    AbstractParameter,
    ParameterValueChoiceTypeMixin,
):
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
    resourceType = Field("Parameters", const=True)
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
