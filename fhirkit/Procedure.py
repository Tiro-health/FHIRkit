try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type:ignore
from typing import Optional, Union, List, Sequence
from pydantic import Field, validator
from fhirkit.choice_type import deterimine_choice_type, ChoiceType
from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Reference,
    Annotation,
    BackboneElement,
)
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Practitioner import Practitioner
from fhirkit.Organization import Organization


ProcedureStatus = Literal[
    "preparation",
    "in-progress",
    "not-done",
    "on-hold",
    "stopped",
    "completed",
    "entered-in-error",
    "unknown",
]


class ProcedurePerformer(BackboneElement):
    function: Optional[CodeableConcept] = Field(None, repr=True)
    actor: Reference
    onBehalfOf: Optional[Reference] = Field(None, repr=True)


class Procedure(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Procedure"] = Field("Procedure", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    partOf: Optional[List[Reference]] = Field([], repr=True)
    status: ProcedureStatus = Field("completed", repr=True)
    statusReason: Optional[CodeableConcept] = Field(None, repr=True)
    category: Optional[CodeableConcept] = Field(None, repr=True)
    code: Optional[CodeableConcept] = Field(None, repr=True)
    subject: Reference
    encounter: Optional[Reference] = Field(None, repr=True)
    reasonReference: Optional[List[Reference]] = Field([], repr=True)
    bodySite: Optional[List[CodeableConcept]] = Field([], repr=True)
    complication: Optional[List[CodeableConcept]] = Field(None, repr=True)
    complicationDetail: Optional[List[Reference]] = Field([], repr=True)
    note: Optional[List[Annotation]] = Field([], exclude=True)
    performedDateTime: Optional[dateTime] = Field(None, exclude=True)
    performedPeriod: Optional[Period] = Field(None, exclude=True)
    performedString: Optional[str] = Field(None, exclude=True)
    performedAge: Optional[int] = Field(None, exclude=True)
    performed: Optional[Union[dateTime, Period, str, int]] = ChoiceType(None)
    asserter: Optional[Practitioner] = Field(None, repr=True)
    performer: Optional[Sequence[ProcedurePerformer]] = Field([], repr=True)
    location: Optional[Reference] = Field(None, repr=True)
   
    @validator("performed", pre=True, always=True, allow_reuse=True)
    def validate_performed(cls, v, values, field):
        return deterimine_choice_type(
            cls,
            v,
            values,
            field,
        )
