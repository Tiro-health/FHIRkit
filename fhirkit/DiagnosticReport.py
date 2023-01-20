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
)

DiagnosticReportStatus = Literal[
    "registered",
    "partial",
    "preliminary"
    "final",
]

class DiagnosticReport(DomainResource):
    resourceType: Literal["DiagnosticReport"] = Field("DiagnosticReport", const=True)
    identifier: Optional[List[Identifier]] = Field(None)
    basedOn: Optional[List[Reference]] = Field(None)
    status: Optional[DiagnosticReportStatus] = Field(None)
    category: Optional[List[CodeableConcept]] = Field(None)
    code: Optional[CodeableConcept] = Field(None)
    subject: Optional[Reference] = Field(None)
    encounter: Optional[Reference] = Field(None)
    effectiveDateTime: Optional[datetime] = Field(None)
    effectivePeriod: Optional[Period] = Field(None)
    effective: Optional[Union[datetime, Period,str]] = ChoiceType(None)
    issued: Optional[datetime] = Field(None)
    performer: Optional[List[Reference]] = Field(None)
    resultsInterpreter: Optional[List[Reference]] = Field(None)
    specimen: Optional[List[Reference]] = Field(None)
    result: Optional[List[Reference]] = Field(None)
    conclusion: Optional[str] = Field(None)
    conclusionCode: Optional[List[CodeableConcept]] = Field(None)


