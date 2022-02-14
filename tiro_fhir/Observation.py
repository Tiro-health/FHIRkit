from datetime import datetime
from typing import Literal, Optional, Sequence

from pydantic import BaseModel, Field
from tiro_fhir.Resource import DomainResource
from tiro_fhir.data_types import Code
from tiro_fhir.elements import CodeableConcept, Identifier, Quantity, Reference, BackboneElement

# TODO find better solution for multitype value
class ObservationValueChoiceTypeMixin(BaseModel):
    valueString: Optional[str]
    valueQuantity: Optional[Quantity]
    valueInteger: Optional[int]
    valueCodeableConcept: Optional[CodeableConcept]
    valueBoolean: Optional[bool]

    def __repr_args__(self):
        return [(k, v) for k, v in super().__repr_args__() if not k.startswith("value") or v is not None]

class ObservationComponent(BackboneElement, ObservationValueChoiceTypeMixin):
    code: CodeableConcept

class Observation(DomainResource, ObservationValueChoiceTypeMixin):

    resourceType = Field("Observation", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    status: Literal["registered", "preliminary", "final", "amended", "corrected", "cancelled", "enterred-in-error", "unknown"] = Field("final", repr=True)
    category: Optional[CodeableConcept] = Field(None, repr=True)
    code: CodeableConcept = Field(..., repr=True)
    subject: Optional[Reference]
    encounter: Optional[Reference]
    effectiveDateTime: Optional[datetime] = Field(None, repr=True)

    method: Optional[Code] = Field(None, repr=False)
    derivedFrom: Optional[Reference]

    component: Sequence[ObservationComponent] = []
    
