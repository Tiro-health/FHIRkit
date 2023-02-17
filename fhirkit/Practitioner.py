try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field
from typing import Optional, Sequence
from fhirkit import Reference
from fhirkit.Resource import DomainResource
from fhirkit.elements import (
    dateTime,
    HumanName,
    Identifier,
    ContactPoint,
    Address,
    AdministrativeGender,
    Attachment,
    Period,
    BackboneElement,
    CodeableConcept
)

class PractitionerQualification(BackboneElement):
    identifier: Optional[Sequence[Identifier]] = Field(
        None,
        title="An identifier for this qualification for the practitioner")
    code: CodeableConcept = Field(
        None,
        title="Coded representation of the qualification")
    period: Optional[Period] = Field(
        None,
        title="Period during which the qualification is valid")
    issuer: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="Organization that regulates and issues the qualification")
        
class Practitioner(DomainResource):
    resourceType: Literal["Practitioner"] = Field(
        "Practitioner", 
        const=True)
    identifier: Optional[Sequence[Identifier]] = Field(
        None,
        title="External Identifiers for this procedure")    
    active: Optional[bool] = Field(
        None,
        title="Whether this practitioner's record is in active use")
    name: Optional[Sequence[HumanName]] = Field(
        None,
        title="The name(s) associated with the practitioner")
    telecom: Optional[Sequence[ContactPoint]] = Field(
        None,
        title="A contact detail for the practitioner (that apply to all roles)")
    address: Optional[Sequence[Address]] = Field(
        None,
        title="Address(es) of the practitioner that are not role specific (typically home address)")
    gender: Optional[AdministrativeGender] = Field(
        None,
        title="male | female | other | unknown")
    birthDate: Optional[dateTime] = Field(
        None,
        title="The date of birth for the practitioner")
    photo: Optional[Attachment] = Field(
        None,
        title="Image of the person")
    qualification: Optional[Sequence["PractitionerQualification"]] = Field(
        None,
        title="Certification, licenses, or training pertaining to the provision of care")
    communication: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="A language the practitioner is able to use in patient communication")
