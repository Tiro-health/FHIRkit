try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from typing import Optional, Sequence, List
from pydantic import Field


from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements import (
    CodeableConcept,
    Coding,
    Reference,
    Identifier,
)
from fhirkit.elements.elements import BackboneElement


EncounterStatus = Literal[
    "planned",
    "arrived",
    "triaged",
    "in-progress",
    "onleave",
    "finished",
    "cancelled",
]

EncounterClass = Literal[
    "AMB",
    "EMER",
    "FLD",
    "HH",
    "IMP",
    "ACUTE",
    "NONAC",
    "OBSENC",
    "PRENC",
    "SS",
    "VR",
]


class EncounterHospitalization(BackboneElement):
    preAdmissionIdentifier: Optional[Identifier] = Field(None, repr=True)
    origin: Optional[Reference] = Field(None, repr=True)
    admitSource: Optional[CodeableConcept] = Field(None, repr=True)
    reAdmission: Optional[CodeableConcept] = Field(None, repr=True)
    destination: Optional[Reference] = Field(None, repr=True)
    dischargeDisposition: Optional[CodeableConcept] = Field(None, repr=True)


class Encounter(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Encounter"] = Field("Encounter", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    status: EncounterStatus = Field("planned", repr=True)
    subject: Optional[List[Reference]] = Field(None, repr=True)
    reasonCode: Optional[List[CodeableConcept]] = Field([], repr=True)
    reasonReference: Optional[List[Reference]] = Field([], repr=True)
    type: Optional[List[CodeableConcept]] = Field([], repr=True)
    length: Optional[str] = Field(None, repr=True)
    hospitalization: Optional[EncounterHospitalization] = Field(None, exclude=True)
    class_: Coding = Field(Coding(code="AMB",system= "http://hl7.org/fhir/v3/ActCode"), repr=True, alias='class')
    priority: Optional[CodeableConcept] = Field(None, repr=True)
