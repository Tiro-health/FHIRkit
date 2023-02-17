from typing import Optional, Sequence
from pydantic import Field
from fhirkit.elements import ContactPoint, Element, CodeableConcept, HumanName,Address,AdministrativeGender,Reference,Period


class ContactDetail(Element):
    relationship: Optional[Sequence[CodeableConcept]] = Field(
        None, 
        title="The kind of relationship")
    name: Optional[HumanName]= Field(
        None,
        title="A name associated with the contact")
    telecom: Optional[Sequence[ContactPoint]] = Field(
        None,
        title="A contact detail for the person")
    address: Optional[Address] = Field(
        None,
        title="Address for the contact person")
    gender: Optional[AdministrativeGender] = Field(
        None,
        title="male | female | other | unknown")
    organization: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="Organization that is associated with the contact")
    period: Optional[Period] = Field(
        None,
        title="Time period when the contact detail is applicable")

