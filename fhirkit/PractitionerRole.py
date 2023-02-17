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
    CodeableConcept,
    DaysOfWeek,
)

class AvailableTime(BackboneElement):
    daysOfWeek: Optional[Sequence[DaysOfWeek]] = Field(
        None,
        title="mon | tue | wed | thu | fri | sat | sun")
    allDay: Optional[bool] = Field(
        None,
        title="Always available? e.g. 24 hour service")
    availableStartTime: Optional[dateTime] = Field(
        None,
        title="Opening time of day (ignored if allDay = true)")
    availableEndTime: Optional[dateTime] = Field(
        None,
        title="Closing time of day (ignored if allDay = true)")


class NotAvailable(BackboneElement):
    description: str = Field(
        None,
        title="Reason presented to the user explaining why time not available")
    during: Optional[Period] = Field(
        None,
        title="Service not available from this date")

class PractitionerRole(DomainResource):
    resourceType: Literal["PractitionerRole"] = Field(
        "PractitionerRole", 
        const=True)
    identifier: Optional[Sequence[Identifier]] = Field(
        None,
        title="An identifier for this patient")
    active: Optional[bool] = Field(
        None,
        title="Whether this practitioner's record is in active use")
    period: Optional[Period] = Field(
        None,
        title="The period during which the practitioner is authorized to perform in these role(s)")
    practitioner: Optional[Reference] = Field(
        None,
        enum_reference_types=["Practitioner"],
        title="Practitioner that is able to provide the defined services for the organization")
    organization: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="Organization where the roles are available")
    code: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="Roles which this practitioner may perform",
        valueset="http://hl7.org/fhir/ValueSet/practitioner-role")
    specialty: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="Specific specialty of the practitioner",
        valueset="http://hl7.org/fhir/ValueSet/c80-practice-codes")
    location: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["Location"],
        title="The location(s) at which this practitioner provides care")
    healthcareService: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["HealthcareService"],
        title="The list of healthcare services that this worker provides for this role's Organization/Location(s)")
    telecom: Optional[Sequence[ContactPoint]] = Field(
        None,
        title="Contact details that are specific to the role/location/service")
    availableTime: Optional[Sequence[AvailableTime]] = Field(
        None,
        title="Times the Service Site is available")
    notAvailable: Optional[Sequence[NotAvailable]] = Field(
        None,
        title="Not available during this time due to provided reason")
    availabilityExceptions: Optional[str] = Field(
        None,
        title="Description of availability exceptions")
    endpoint: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["Endpoint"],
        title="Technical endpoints providing access to services operated for the practitioner with this role")
    
    

    
    
    
