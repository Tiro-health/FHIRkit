
from datetime import datetime
from typing import Literal, Optional

from pydantic import Field
from tiro_fhir.Resource import DomainResource
from tiro_fhir.elements import CodeableConcept, Identifier, Reference

class Procedure(DomainResource):
    resourceType = Field("Procedure", const=True)
    identifier:Optional[Identifier] = Field(None, repr=True)
    status: Literal["preparation", "in-progress", "not-done", "on-hold", "stopped", "completed", "entered-in-error", "unknown"] = Field("completed", repr=True)
    statusReason: Optional[CodeableConcept] = Field(None, repr=True)
    category: Optional[CodeableConcept] = Field(None, repr=True)
    code: Optional[CodeableConcept] = Field(None, repr=True)
    subject: Reference
    encounter: Optional[Reference] = Field(None, repr=True)
    performedDateTime: Optional[datetime] = Field(None, repr=True)
    