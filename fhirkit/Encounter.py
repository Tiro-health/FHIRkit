try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from typing import Optional
from pydantic import Field


from fhirkit.Resource import DomainResource
from .elements.elements import CodeableConcept, Reference,Identifier,Hospitalization


EncounterStatus: Literal[
        "planned",
        "arrived",
        "triaged",
        "in-progress",
        "onleave",
        "finished",
        "cancelled",
    ]

EncounterClass: Literal[
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
class Encounter(DomainResource):
    resourceType: Literal["Encounter"] = Field("Encounter", const=True)
    identifier: Optional[Identifier] = Field(None, repr=True)
    status: EncounterStatus = Field("completed", repr=True)
    subject: Optional[Reference] = None
    reasonCode: Optional[CodeableConcept] = None
    reasonReference: Optional[Reference] = None
    type: Optional[CodeableConcept] = None
    #TODO add http://hl7.org/fhir/ValueSet/all-time-units
    length: Optional[str] = None
    hospitalization: Optional[Hospitalization] = Field(None, exclude=True)
    class_: EncounterStatus = Field("AMB", repr=True)
    priority: Optional[CodeableConcept] = None