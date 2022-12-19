try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from pydantic import Field


from fhirkit.Resource import DomainResource
from typing import Optional, Union, List, Sequence
from pydantic import Field, validator
from fhirkit.choice_type import deterimine_choice_type, ChoiceType
from fhirkit.Resource import DomainResource
from fhirkit.elements import CodeableConcept, Identifier, Period, Reference, Annotation, BackboneElement
from fhirkit.elements.elements import Address, ContactPoint
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Practitioner import Practitioner
from fhirkit.Organization import Organization


LocationStatus = Literal[
    "active",
    "suspended",
    "inactive",
]
LocationMode = Literal[
    "instance",
    "kind",
]
class Location(DomainResource):
    resourceType: Literal["Location"] = Field("Location", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    status: Optional[LocationStatus] = Field("active", repr=True)
    name: Optional[str] = Field(None, repr=True)
    alias: Optional[List[str]] = Field(None, repr=True)
    description: Optional[str] = Field(None, repr=True)
    mode: Optional[LocationStatus] = Field(None, repr=True)
    type: Optional[List[CodeableConcept]] = Field(None, repr=True)
    telecom: Optional[List[ContactPoint]] = Field(None, repr=True)
    address: Optional[Address] = Field(None, repr=True)
    physicalType: Optional[CodeableConcept] = Field(None, repr=True)
    managingOrganization: Optional[Organization] = Field(None, repr=True)

