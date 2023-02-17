try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type:ignore
from typing import Optional, Union, Sequence
from pydantic import Field, validator,AnyUrl
from fhirkit.choice_type import deterimine_choice_type, ChoiceType
from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Reference,
    Age,
    Range,
    Period,
    BackboneElement,
    Annotation
)
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements.elements import Identifier

class ConditionStage(BackboneElement):
    summary: Optional[CodeableConcept] = Field(
        None,
        title="Simple summary (disease specific)")
    assessment: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["ClinicalImpression","DiagnosticReport","Observation"],
        title="Formal record of assessment")
    type: Optional[CodeableConcept] = Field(
        None,
        title="Kind of staging")

class ConditionEvidence(BackboneElement):
    code: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="Manifestation/symptom")
    detail: Optional[Sequence[Reference]] = Field(
        None,
        enum_reference_types=["Any"],
        title="Supporting information found elsewhere")


class Condition(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Condition"] = Field(
        "Condition", 
        const=True)
    identifier: Sequence[Identifier] = Field(
        None,
        title="External Ids for this condition")
    clinicalStatus: Optional[CodeableConcept] = Field(
        None,
        title="active | recurrence | relapse | inactive | remission | resolved",
        valueset="http://hl7.org/fhir/ValueSet/condition-clinical")
    verificationStatus: Optional[CodeableConcept] = Field(
        None,
        title="unconfirmed | provisional | differential | confirmed | refuted | entered-in-error",
        valueset="http://hl7.org/fhir/ValueSet/condition-ver-status")
    category: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="problem-list-item | encounter-diagnosis",
        valueset="http://hl7.org/fhir/ValueSet/condition-category")
    severity: Optional[CodeableConcept] = Field(
        None,
        title="Subjective severity of condition",
        valueset="http://hl7.org/fhir/ValueSet/condition-severity")
    code: Optional[CodeableConcept] = Field(
        None,
        title="Identification of the condition, problem or diagnosis")
    bodySite: Optional[Sequence[CodeableConcept]] = Field(
        None,
        title="Anatomical location, if relevant")
    subject: Optional[Reference] = Field(
        None,
        enum_reference_types=["Patient","Group"],
        title="Who has the condition?")
    encounter: Optional[Reference] = Field(
        None,
        enum_reference_types=["Encounter"],
        title="Encounter created as part of")
    onsetDateTime: Optional[dateTime] = Field(
        None, 
        exclude=True)
    onsetAge: Optional[Age] = Field(
        None, 
        exclude=True)
    onsetPeriod: Optional[Period] = Field(
        None, 
        exclude=True)
    onsetRange: Optional[Range] = Field(
        None, 
        exclude=True)
    onsetString: Optional[str] = Field(
        None, 
        exclude=True)
    onset: Optional[Union[dateTime, Age, Period, Range, str]] = ChoiceType(
        None,
        title="Estimated or actual date, date-time, or age")
    abatementDateTime: Optional[dateTime] = Field(
        None, 
        exclude=True)
    abatementAge: Optional[Age] = Field(
        None, 
        exclude=True)
    abatementPeriod: Optional[Period] = Field(
        None, 
        exclude=True)
    abatementRange: Optional[Range] = Field(
        None, 
        exclude=True)
    abatementString: Optional[str] = Field(
        None, 
        exclude=True)
    abatement: Optional[Union[dateTime, Age, bool, Period, Range, str]] = ChoiceType(
        None,
        title="When in resolution/remission")
    recordedDate: Optional[dateTime] = Field(
        None,
        title="Date record was first recorded")
    recorder: Optional[Reference] = Field(
        None,
        enum_reference_types=["Practitioner","PractitionerRole","Patient","RelatedPerson"],
        title="Who recorded the condition?")
    asserter: Optional[Reference] = Field(
        None,
        enum_reference_types=["Practitioner","PractitionerRole","Patient","RelatedPerson"],
        title="Person who asserts this condition")
    stage: Optional[Sequence[ConditionStage]] = Field(
        None,
        title="Stage/grade, usually assessed formally")
    evidence: Optional[Sequence[ConditionEvidence]] = Field(
        None,
        title="Supporting evidence")
    note: Optional[Sequence[Annotation]] = Field(
        None,
        title="Additional information about the Condition")


    @validator("onset", pre=True, always=True, allow_reuse=True)
    def validate_performed(cls, v, values, field):
        return deterimine_choice_type(
            cls,
            v,
            values,
            field,
        )
    @validator("abatement", pre=True, always=True, allow_reuse=True)
    def validate_performed(cls, v, values, field):
        return deterimine_choice_type(
            cls,
            v,
            values,
            field,
        )
