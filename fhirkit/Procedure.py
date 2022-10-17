try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type:ignore
from typing import Optional, Union, List
from pydantic import Field, validator
from fhirkit.choice_type import deterimine_choice_type
from fhirkit.Resource import DomainResource
from fhirkit.elements import CodeableConcept, Identifier, Period, Reference, Annotation
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Practitioner import Practitioner


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


class Procedure(DomainResource):
    resourceType: Literal["Procedure"] = Field("Procedure", const=True)
    identifier: Optional[Identifier] = Field(None, repr=True)
    partOf: Optional[List[Reference]] = Field(None, repr=True)
    status: ProcedureStatus = Field("completed", repr=True)
    statusReason: Optional[CodeableConcept] = Field(None, repr=True)
    category: Optional[CodeableConcept] = Field(None, repr=True)
    code: Optional[CodeableConcept] = Field(None, repr=True)
    subject: Reference
    encounter: Optional[Reference] = Field(None, repr=True)
    reason: Optional[Reference] = Field(None, repr=True)
    bodySite: Optional[CodeableConcept] = Field(None, exclude=True)
    complication: Optional[CodeableConcept] = Field(None, exclude=True)
    note: Optional[Annotation] = Field(None, exclude=True)
    # Custom fields
    performedDateTime: Optional[dateTime] = Field(None, exclude=True)
    performedPeriod: Optional[Period] = Field(None, exclude=True)
    performedString: Optional[str] = Field(None, exclude=True)
    performed: Union[dateTime, Period, str] = Field(None, repr=True)
    performedAge: Optional[int] = Field(None, exclude=True)
    asserter: Optional[Practitioner] = Field(None, exclude=True)

    @validator("performed", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values, field):
        return deterimine_choice_type(
            cls,
            v,
            values,
            field,
        )
