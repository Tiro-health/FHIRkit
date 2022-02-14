from typing import Literal, Optional, Sequence

from pydantic import BaseModel, Field
from tiro_fhir.Resource import DomainResource
from tiro_fhir.data_types import Code
from tiro_fhir.elements import CodeableConcept, Identifier, Quantity, Reference


class ObservationComponent(BaseModel):
    code: CodeableConcept
    valueString: Optional[str]
    valueQuantity: Optional[Quantity]
    valueInteger: Optional[int]
    valueCodeableConcept: Optional[CodeableConcept]
    valueBoolean: Optional[bool]

class Observation(DomainResource):
    resourceType = Field("Observation", const=True)
    identifier: Sequence[Identifier] = []
    status: Literal["registered", "preliminary", "final", "amended", "corrected", "cancelled", "enterred-in-error", "unknown"] = "final"
    category: Optional[CodeableConcept]
    code: CodeableConcept
    subject: Optional[Reference]
    encounter: Optional[Reference]

    valueString: Optional[str]
    valueQuantity: Optional[Quantity]
    valueInteger: Optional[int]
    valueCodeableConcept: Optional[CodeableConcept]
    valueBoolean: Optional[bool]
    method: Optional[Code]
    derivedFrom: Optional[Reference]