from typing import Optional, Sequence, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


from pydantic import BaseModel, Field, validator
from fhirkit.ChoiceTypeMixin import validate_choice_types
from fhirkit.Resource import DomainResource
from fhirkit.data_types import Code, dateTime, time
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Quantity,
    Range,
    Ratio,
    Reference,
    BackboneElement,
)

# TODO find better solution for multitype value
class ObservationValueChoiceTypeMixin(BaseModel):

    valueString: Optional[str] = Field(None, exclude=True, repr=False)
    valueQuantity: Optional[Quantity] = Field(None, exclude=True, repr=False)
    valueInteger: Optional[int] = Field(None, exclude=True, repr=False)
    valueCodeableConcept: Optional[CodeableConcept] = Field(
        None, exclude=True, repr=False
    )
    valueBoolean: Optional[bool] = Field(None, exclude=True, repr=False)
    valueRange: Optional[Range] = Field(None, exclude=True, repr=False)
    valueRatio: Optional[Ratio] = Field(None, exclude=True, repr=False)
    valueTime: Optional[time] = Field(None, exclude=True, repr=False)
    valueDateTime: Optional[dateTime] = Field(None, exclude=True, repr=False)
    valuePeriod: Optional[Period] = Field(None, exclude=True, repr=False)

    value: Union[
        str, Quantity, int, CodeableConcept, bool, Range, Ratio, time, dateTime, Period
    ] = None

    @validator("value", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values):
        return validate_choice_types(
            cls,
            v,
            values,
            {
                "valueString",
                "valueQuantity",
                "valueInteger",
                "valueCodeableConcept",
                "valueBoolean",
            },
            "value",
        )


class ObservationComponent(BackboneElement, ObservationValueChoiceTypeMixin):

    code: CodeableConcept


class Observation(
    DomainResource,
    ObservationValueChoiceTypeMixin,
):

    resourceType: Literal["Observation"] = Field("Observation", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    status: Literal[
        "registered",
        "preliminary",
        "final",
        "amended",
        "corrected",
        "cancelled",
        "enterred-in-error",
        "unknown",
    ] = Field("final", repr=True)
    category: Sequence[CodeableConcept] = Field([], repr=True)
    code: CodeableConcept = Field(..., repr=True)
    subject: Optional[Reference]
    encounter: Optional[Reference]

    method: Optional[Code] = Field(None, repr=False)
    derivedFrom: Optional[Reference]

    component: Sequence[ObservationComponent] = []

    effectiveDateTime: Optional[dateTime] = Field(None, exclude=True, repr=False)
    effectivePeriod: Optional[Period] = Field(None, exclude=True, repr=False)
    effective: Union[dateTime, Period] = None

    @validator("effective", pre=True, always=True, allow_reuse=True)
    def validate_effective(cls, v, values):
        return validate_choice_types(
            cls, v, values, ["effectiveDateTime", "effectivePeriod"], "effective"
        )
