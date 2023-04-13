try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from pydantic import Field, validator
from typing import Optional, Sequence, Union, List
from fhirkit.choice_type import deterimine_choice_type, ChoiceType
from fhirkit.primitive_datatypes import dateTime, date
from fhirkit.Resource import DomainResource
from fhirkit.metadata_types import ContactDetail, ContactPoint
from fhirkit.elements import (
    CodeableConcept,
    HumanName,
    Identifier,
    Reference,
    Address,
    AdministrativeGender,
    Attachment,
    BackboneElement,
    Link
)


class PatientCommunication(BackboneElement):
    language: CodeableConcept = Field(
        None,
        title="The language which can be used to communicate with the patient about his or her health")
    preferred: Optional[bool] = Field(
        None,
        title="Language preference indicator")
class Patient(DomainResource):
    resourceType: Literal["Patient"] = Field(
        "Patient", 
        const=True)
    identifier: Optional[Sequence[Identifier]] = Field(
        None,
        title="An identifier for this patient")
    active: Optional[bool] = Field(
        None,
        title="Whether this patient record is in active use")
    name: Optional[Sequence[HumanName]] = Field(
        None,
        title="A name associated with the patient")
    telecom: Optional[Sequence[ContactPoint]] = Field(
        None,
        title="A contact detail for the individual")
    gender: Optional[AdministrativeGender] = Field(
        None,
        title="male | female | other | unknown")
    birthDate: Optional[date] = Field(
        None,
        title="The date of birth for the individual")
    deceasedBoolean: Optional[bool] = Field(
        None, 
        exclude=False)
    deceasedDateTime: Optional[dateTime] = Field(
        None, 
        exclude=False)
    address: Optional[Sequence[Address]] = Field(
        None,
        title="Addresses for the individual")
    maritalStatus: Optional[CodeableConcept] = Field(
        None,
        title="Marital (civil) status of a patient",
        valueset="http://hl7.org/fhir/ValueSet/marital-status")
    multipleBirthBoolean: Optional[bool] = Field(
        None, 
        exclude=True)
    multipleBirthInteger: Optional[int] = Field(
        None, 
        exclude=True)
    multipleBirth: Optional[Union[bool, int]] = ChoiceType(
        None,
        title="Whether patient is part of a multiple birth")
    photo: Optional[Sequence[Attachment]] = Field(
        None,
        title="Image of the patient")
    contact: Optional[Sequence[ContactDetail]] = Field(
        None,
        title="A contact party (e.g. guardian, partner, friend) for the patient")
    communication: Optional[Sequence[PatientCommunication]] = Field(
        None,
        title="A language which may be used to communicate with the patient about his or her health")
    generalPractitioner: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["Organization","Practitioner","PractitionerRole"],
        title="Patient's nominated primary care provider")
    managingOrganization: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="Organization that is the custodian of the patient record")
    link: Optional[Sequence[Link]] = Field(
        None,
        title="Link to another patient resource that concerns the same actual patient")

