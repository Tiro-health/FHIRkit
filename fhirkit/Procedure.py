from typing import Literal, Optional, Union
from pydantic import BaseModel, Field, ValidationError, validator
from fhirkit.Resource import DomainResource
from fhirkit.elements import CodeableConcept, Identifier, Period, Reference
from fhirkit.data_types import dateTime


class ProcedurePerformedChoiceTypeMixin(BaseModel):
    performedDateTime: Optional[dateTime] = Field(None, exclude=True)
    performedPeriod: Optional[Period] = Field(None, exclude=True)
    performedString: Optional[str] = Field(None, exclude=True)
    performed: Union[dateTime, Period, str] = Field(None, repr=True)

    @validator("performed", pre=True, always=True, allow_reuse=True)
    def determine_performed(cls, v, values):
        if v is not None:
            return v

        # if Procedure.performed[x] is not send through 'value' check other typed field names
        non_null_values = list(
            filter(
                lambda t: t[0].startswith("performed") and t[1] is not None,
                values.items(),
            )
        )
        if len(non_null_values) == 0:
            raise ValidationError("Procedure.performed[x] can not be None.")
        elif len(non_null_values) > 1:
            raise ValidationError("Procedure.performed[x] can only have one value.")
        return non_null_values[0][1]


class Procedure(DomainResource, ProcedurePerformedChoiceTypeMixin):
    resourceType = Field("Procedure", const=True)
    identifier: Optional[Identifier] = Field(None, repr=True)
    status: Literal[
        "preparation",
        "in-progress",
        "not-done",
        "on-hold",
        "stopped",
        "completed",
        "entered-in-error",
        "unknown",
    ] = Field("completed", repr=True)
    statusReason: Optional[CodeableConcept] = Field(None, repr=True)
    category: Optional[CodeableConcept] = Field(None, repr=True)
    code: Optional[CodeableConcept] = Field(None, repr=True)
    subject: Reference
    encounter: Optional[Reference] = Field(None, repr=True)
