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
    Period,
    Duration,
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

class EncounterStatusHistory(BackboneElement):
    status: EncounterStatus = Field(
        "planned",
        title="planned | arrived | triaged | in-progress | onleave | finished | cancelled")
    period: Optional[Period] = Field(
        None,
        title="The time that the episode was in the specified status")

class EncounterClassHistory(BackboneElement):
    class_: Coding = Field(
        Coding(code="AMB",system= "http://hl7.org/fhir/v3/ActCode"), 
        alias='class',
        title="inpatient | outpatient | ambulatory | emergency +")
    period: Period = Field(
        None,
        title="Time period during which the patient was in the specified class")

class EncounterParticipant(BackboneElement):
    type: Optional[List[CodeableConcept]] = Field(
        None,
        title="Role of participant in encounter",
        valueset="http://hl7.org/fhir/ValueSet/encounter-participant-type")
    period: Optional[Period] = Field(
        None,
        title="Period of time during the encounter that the participant participated")
    individual: Optional[Reference] = Field(
        None,
        enum_reference_types=["Practitioner","PractitionerRole","RelatedPerson"],
        title="Persons involved in the encounter other than the patient")

class EncounterDiagnosis(BackboneElement):
    condition: Reference = Field(
        None,
        enum_reference_types=["Condition"],
        title="The diagnosis or procedure relevant to the encounter")
    use: Optional[CodeableConcept] = Field(
        None,
        title="Role that this diagnosis has within the encounter (e.g. admission, billing, discharge …)",
        valueset="http://hl7.org/fhir/ValueSet/diagnosis-role")
    rank: Optional[int] = Field(
        None,
        title="Ranking of the diagnosis (for each role type)")

class EncounterHospitalization(BackboneElement):
    preAdmissionIdentifier: Optional[Identifier] = Field(
        None,
        title="Pre-admission identifier")
    origin: Optional[Reference] = Field(
        None,
        enum_reference_types=["Location","Organization"],
        title="The location/organization from which the patient came before admission")
    admitSource: Optional[CodeableConcept] = Field(
        None,
        title="From where patient was admitted (physician referral, transfer)",
        valueset="http://hl7.org/fhir/ValueSet/encounter-admit-source")
    reAdmission: Optional[CodeableConcept] = Field(
        None,
        title="The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission",
        valueset="http://terminology.hl7.org/ValueSet/v2-0092")
    destination: Optional[Reference] = Field(
        None,
        enum_reference_types=["Location","Organization"],
        title="Location/organization to which the patient is discharged")
    dischargeDisposition: Optional[CodeableConcept] = Field(
        None,
        title="Category or kind of location after discharge",
        valueset="http://hl7.org/fhir/ValueSet/encounter-discharge-disposition")

class EncounterLocation(BackboneElement):
    location: Reference = Field(
        None,
        enum_reference_types=["Location"],
        title="Location the encounter takes place")
    status: Optional[EncounterStatus] = Field(
        None,
        title="planned | active | reserved | completed")
    period: Optional[Period] = Field(
        None,
        title="Time period during which the patient was present at the location")

class Encounter(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Encounter"] = Field(
        "Encounter", 
        const=True)
    identifier: Sequence[Identifier] = Field(
        None,
        title="Identifier(s) by which this encounter is known")
    status: EncounterStatus = Field(
        "planned",
        title="planned | arrived | triaged | in-progress | onleave | finished | cancelled")
    statusHistory: Optional[List[EncounterStatusHistory]] = Field(
        None,
        title="List of past encounter statuses")
    class_: Coding = Field(
        Coding(code="AMB",system= "http://hl7.org/fhir/v3/ActCode"), 
        alias='class',
        title="Classification of patient encounter")
    classHistory: Optional[List[EncounterClassHistory]] = Field(
        None,
        title="List of past encounter classes")
    type: Optional[List[CodeableConcept]] = Field(
        None,
        title="Specific type of encounter",
        valueset="http://hl7.org/fhir/ValueSet/encounter-type")
    serviceType: Optional[CodeableConcept] = Field(
        None,
        title="Specific type of service")
    priority: Optional[CodeableConcept] = Field(
        None,
        title="Indicates the urgency of the encounter",
        valueset="http://terminology.hl7.org/ValueSet/v3-ActPriority")
    subject: Optional[Reference] = Field(
        None,
        enum_reference_types=["Patient","Group"],
        title="The patient or group present at the encounter")
    episodeOfCare: Optional[List[Reference]] = Field(
        None,enum_reference_types=["EpisodeOfCare"],
        title="Episode(s) of care that this encounter should be recorded against")
    basedOn: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["ServiceRequest"],
        title="The ServiceRequest that initiated this encounter")
    participant:  Optional[EncounterParticipant] = Field(
        None,
        title="List of participants involved in the encounter")
    appointment: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["Appointment"],
        title="The appointment that scheduled this encounter")
    period: Optional[Period] = Field(
        None,
        title="The start and end time of the encounter")
    length: Optional[Duration] = Field(
        None,
        title="Quantity of time the encounter lasted (less time absent)")
    reasonCode: Optional[List[CodeableConcept]] = Field(
        None,
        title="Coded reason the encounter takes place",
        valueset="http://hl7.org/fhir/ValueSet/encounter-reason")
    reasonReference: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["Condition","Procedure","Observation","ImmunizationRecommendation"],
        title="Reason the encounter takes place (reference)")
    diagnosis: Optional[List[EncounterDiagnosis]] = Field(
        None,
        title="The list of diagnosis relevant to this encounter")
    account: Optional[List[Reference]] = Field(
        None,enum_reference_types=["Account"],
        title="The set of accounts that may be used for billing for this Encounter")
    hospitalization: Optional[EncounterHospitalization] = Field(
        None, 
        title="Details about the admission to a healthcare service")
    location: Optional[List[EncounterLocation]] = Field(
        None,
        title="List of locations where  the patient has been")
    serviceProvider: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="The organization (facility) responsible for this encounter")
    partOf: Optional[Reference] = Field(
        None,
        enum_reference_types=["Encounter"],
        title="Another Encounter this encounter is part of")


    

