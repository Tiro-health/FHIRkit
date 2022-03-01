from datetime import datetime
from typing import Literal, Optional, Sequence, Union

from pydantic import BaseModel, Field, ValidationError, validator
from tiro_fhir.Resource import DomainResource
from tiro_fhir.data_types import Code, dateTime
from tiro_fhir.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Quantity,
    Reference,
    BackboneElement,
)

# TODO find better solution for multitype value
class ObservationValueChoiceTypeMixin(BaseModel):
    valueString: Optional[str] = Field(None, exclude=True)
    valueQuantity: Optional[Quantity] = Field(None, exclude=True)
    valueInteger: Optional[int] = Field(None, exclude=True)
    valueCodeableConcept: Optional[CodeableConcept] = Field(None, exclude=True)
    valueBoolean: Optional[bool] = Field(None, exclude=True)
    value: Union[str, Quantity, int, CodeableConcept, bool] = None

    @validator("value", pre=True, always=True)
    def determine_value(cls, v, values):
        if v is not None:
            return v

        # if Observation.value[x] is not send through 'value' check other typed field names
        non_null_values = list(
            filter(
                lambda t: t[0].startswith("value") and t[1] is not None, values.items()
            )
        )
        if len(non_null_values) == 0:
            raise ValidationError("Observation.value[x] can not be None.")
        elif len(non_null_values) > 1:
            raise ValidationError("Observation.value[x] can only have one value.")
        return non_null_values[0][1]


class ObservationEffectiveChoiceTypeMixin(BaseModel):
    effectiveDateTime: Optional[dateTime] = Field(None, exclude=True)
    effectivePeriod: Optional[Period] = Field(None, exclude=True)
    effective: Union[dateTime, Period] = None

    @validator("effective", pre=True, always=True)
    def determine_effective(cls, v, values):
        if v is not None:
            return v

        # if Observation.effective[x] is not send through 'value' check other typed field names
        non_null_values = list(
            filter(
                lambda t: t[0].startswith("effective") and t[1] is not None,
                values.items(),
            )
        )
        if len(non_null_values) == 0:
            raise ValidationError("Observation.effective[x] can not be None.")
        elif len(non_null_values) > 1:
            raise ValidationError("Observation.effective[x] can only have one value.")
        return non_null_values[0][1]


class ObservationComponent(BackboneElement, ObservationValueChoiceTypeMixin):
    code: CodeableConcept


class Observation(
    DomainResource, ObservationValueChoiceTypeMixin, ObservationEffectiveChoiceTypeMixin
):

    resourceType = Field("Observation", const=True)
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
    category: Optional[CodeableConcept] = Field(None, repr=True)
    code: CodeableConcept = Field(..., repr=True)
    subject: Optional[Reference]
    encounter: Optional[Reference]

    method: Optional[Code] = Field(None, repr=False)
    derivedFrom: Optional[Reference]

    component: Sequence[ObservationComponent] = []
