try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field
from typing import Optional, Sequence, List

from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    ContactPoint,
    Address,
    Reference,
)


class Organization(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Organization"] = Field("Organization", const=True)
    identifier: Sequence[Identifier] = Field([], repr=True)
    active: Optional[bool] = Field(None, repr=True)
    type: Optional[List[CodeableConcept]] = Field([], repr=True)
    name: Optional[str] = Field(None, repr=True)
    alias: Optional[List[str]] = Field([], repr=True)
    telecom: Optional[Sequence[ContactPoint]] = Field([], repr=True)
    address: Optional[Sequence[Address]] = Field([], repr=True)
    partOf: Optional[Reference] = Field(None, repr=True)
