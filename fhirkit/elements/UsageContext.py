from typing import Optional, Union

from pydantic import Field, validator
from fhirkit.choice_type.choice_type import ChoiceType
from fhirkit.elements import (
    CodeableConcept,
    Coding,
    Element,
    Quantity,
    Range,
    Reference,
)

from fhirkit.choice_type import deterimine_choice_type


class UsageContext(Element):
    code: Coding
    valueCodeableConcept: Optional[CodeableConcept] = Field(None, exclude=True)
    valueQuantity: Optional[Quantity] = Field(None, exclude=True)
    valueRange: Optional[Range] = Field(None, exclude=True)
    valueReference: Optional[Reference] = Field(None, exclude=True)
    value: Union[CodeableConcept, Quantity, Range, Reference] = ChoiceType(None)

    @validator("value", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, value, values, field):
        return deterimine_choice_type(cls, value, values, field)


UsageContext.update_forward_refs()
