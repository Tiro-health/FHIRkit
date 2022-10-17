try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from typing import Optional, Sequence
from pydantic import Field


from fhirkit.Resource import DomainResource
from fhirkit.elements import (
    CodeableConcept,
    Reference,
    Identifier,
    Hospitalization,
)


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


class Encounter(DomainResource):
    resourceType: Literal["Encounter"] = Field("Encounter", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    status: EncounterStatus = Field("completed", repr=True)
    subject: Optional[Reference] = None
    reasonCode: Sequence[CodeableConcept] = Field([], repr=True)
    reasonReference: Optional[Reference] = None
    type: Sequence[CodeableConcept] = Field([], repr=True)
    # TODO add http://hl7.org/fhir/ValueSet/all-time-units
    length: Optional[str] = None
    hospitalization: Optional[Hospitalization] = Field(None, exclude=True)
    class_: EncounterClass = Field("AMB", repr=True)
    priority: Optional[CodeableConcept] = None
