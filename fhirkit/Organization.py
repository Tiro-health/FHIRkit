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
    HumanName,
    BackboneElement
)

class OrganizationContact(BackboneElement):
    purpose: Optional[CodeableConcept] = Field(
        None,
        title="The type of contact")
    name: Optional[HumanName] = Field(
        None,
        title="A name associated with the contact")
    telecom: Optional[Sequence[ContactPoint]] = Field(
        None,
        title="Contact details (telephone, email, etc.)  for a contact")
    address: Optional[Address] = Field(
        None,
        title="Visiting or postal addresses for the contact")

class Organization(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Organization"] = Field(
        "Organization", 
        const=True)
    identifier: Optional[Sequence[Identifier]] = Field(
        None,
        title="An identifier for this patient")
    active: Optional[bool] = Field(
        None,
        title="Whether this organization's record is in active use")
    type: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="Kind of organization")
    name: Optional[str] = Field(
        None,
        title="Name used for the organization")
    alias: Optional[List[str]] = Field(
        None,
        title="A list of alternate names that the organization is known as, or was known as in the past")
    telecom: Optional[Sequence[ContactPoint]] = Field(
        None,
        title="A contact detail for the organization")
    address: Optional[Sequence[Address]] = Field(
        None,
        title="An address for the organization")
    partOf: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="The organization of which this organization forms a part")
    contact: Optional[Sequence[OrganizationContact]] = Field(
        None,
        title="Contact for the organization for a certain purpose")
    endpoint: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["Endpoint"],
        title="Technical endpoints providing access to services operated for the organization")
