from datetime import datetime  # this is important to have at the top

from typing import List, Optional, Sequence, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

from pydantic import Field
from fhirkit.choice_type import ChoiceType
from fhirkit.Resource import DomainResource
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Reference,
    Annotation,
    BackboneElement
)

ClinicalImpressionStatus = Literal[
    "in-progress",
    "completed",
    "entered-in-error"
]

class ClinicalImpressionFinding(BackboneElement):
    item: Optional[Reference] = ChoiceType(None)
    cause: Optional[str] = Field(None)  

class ClinicalImpression(DomainResource):
    resourceType: Literal["ClinicalImpression"] = Field("ClinicalImpression", const=True)
    identifier: Optional[List[Identifier]] = Field(None)
    status: Optional[ClinicalImpressionStatus] = Field(None)
    code: Optional[CodeableConcept] = Field(None)
    description: Optional[str] = Field(None)
    subject: Optional[Reference] = Field(None)
    encounter: Optional[Reference] = Field(None)
    effectiveDateTime: Optional[datetime] = Field(None)
    effectivePeriod: Optional[Period] = Field(None)
    effective: Optional[Union[datetime, Period,str]] = ChoiceType(None)
    date: Optional[datetime] = Field(None)
    assessor: Optional[Reference] = Field(None)
    previous: Optional[Reference] = Field(None)
    problem: Optional[List[Reference]] = Field(None)
    prognosisCodeableConcept: Optional[List[CodeableConcept]] = Field(None)
    supportingInfo: Optional[List[Reference]] = Field(None)
    note: Optional[List[Annotation]] = Field(None)
    finding: Optional[List[ClinicalImpressionFinding]] = Field(None)
    
    


