from typing import Union

from pydantic import validator
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
    value: Union[Quantity, Range, CodeableConcept, Reference] = None

    @validator("value", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, value, values, field):
        return deterimine_choice_type(cls, value, values, field)


UsageContext.update_forward_refs()
