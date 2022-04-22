from datetime import datetime
from typing import ClassVar, Dict, Literal, Optional, Sequence, Set, Tuple, Union

from pydantic import BaseModel, Field, PrivateAttr, ValidationError, validator
from fhirkit.ChoiceTypeMixin import (
    AbstractChoiceTypeMixin,
    ChoiceTypeMixinBase,
    validate_choice_types,
)
from fhirkit.Resource import DomainResource
from fhirkit.data_types import Code, dateTime
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Quantity,
    Reference,
    BackboneElement,
)

# TODO find better solution for multitype value
class ObservationValueChoiceTypeMixin(ChoiceTypeMixinBase):
    _choice_type_fields: ClassVar[Set[str]] = [
        "valueString",
        "valueQuantity",
        "valueInteger",
        "valueCodeableConcept",
        "valueBoolean",
    ]
    _polymorphic_field: ClassVar[Set[str]] = "value"
    valueString: Optional[str] = None
    valueQuantity: Optional[Quantity] = None
    valueInteger: Optional[int] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueBoolean: Optional[bool] = None
    value: Union[str, Quantity, int, CodeableConcept, bool] = None

    validate_value = validator("value", pre=True, always=True, allow_reuse=True)(
        validate_choice_types
    )


class ObservationEffectiveChoiceTypeMixin(ChoiceTypeMixinBase):
    _choice_type_fields: ClassVar[Set[str]] = ["effectiveDateTime", "effectivePeriod"]
    _polymorphic_field: ClassVar[str] = "effective"
    effectiveDateTime: Optional[dateTime] = None
    effectivePeriod: Optional[Period] = None
    effective: Union[dateTime, Period] = None

    validate_effective = validator(
        "effective", pre=True, always=True, allow_reuse=True
    )(validate_choice_types)


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
