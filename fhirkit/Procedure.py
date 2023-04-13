try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type:ignore
from typing import Optional, Union, List, Sequence
from pydantic import Field, validator,AnyUrl
from fhirkit.choice_type import deterimine_choice_type
from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements import (
    CodeableConcept,
    Identifier,
    Period,
    Reference,
    Annotation,
    BackboneElement,
    Range
)
from fhirkit.primitive_datatypes import dateTime,URI
from fhirkit.Practitioner import Practitioner


ProcedureStatus = Literal[
    "preparation",
    "in-progress",
    "not-done",
    "on-hold",
    "stopped",
    "completed",
    "entered-in-error",
    "unknown",
]


class ProcedurePerformer(BackboneElement):
    function: Optional[CodeableConcept] = Field(
        None,
        title="Type of performance")
    actor: Reference = Field(
        None,
        enum_reference_types=["Practitioner","PractitionerRole","Organization","Patient","RelatedPerson","Device"],
        title="The reference to the practitioner")
    onBehalfOf: Optional[Reference] = Field(
        None,
        enum_reference_types=["Organization"],
        title="Organization the device or practitioner was acting for")

class ProcedureFocalDevice(BackboneElement):
    action: Optional[CodeableConcept] = Field(
        None,
        title="Kind of change to device")
    manipulated: Reference = Field(
        None,
        enum_reference_types=["Device"],
        title="Device that was changed")

class Procedure(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Procedure"] = Field(
        "Procedure", 
        const=True)
    identifier: Optional[Sequence[Identifier]] = Field(
        None,
        title="External Identifiers for this procedure")
    instantiatesCanonical: Optional[List[AnyUrl]] = Field(
        None,
        title="Instantiates FHIR protocol or definition",
        enum_canonical_types=["PlanDefinition","ActivityDefinition","Measure","OperationDefinition","Questionnaire"])
    instantiatesUri: Optional[List[URI]] = Field(
        None)
    basedOn: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["CarePlan","ServiceRequest"],
        title="A request for this procedure")
    partOf: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["Procedure","Observation","MedicationAdministration"],
        title="Part of referenced event")
    status: ProcedureStatus = Field(
        None,
        title="preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown",
        valueset="http://hl7.org/fhir/ValueSet/event-status")
    statusReason: Optional[CodeableConcept] = Field(
        None,
        title="Reason for current status")
    category: Optional[CodeableConcept] = Field(
        None,
        title="Classification of the procedure")
    code: Optional[CodeableConcept] = Field(
        None,
        title="Identification of the procedure")
    subject: Reference = Field(
        None,
        enum_reference_types=["Patient","Group"],
        title="Who the procedure was performed on")
    encounter: Optional[Reference] = Field(
        None,
        enum_reference_types=["Encounter"],
        title="Encounter created as part of")
    #performedDateTime: Optional[dateTime] = Field(
    #    None, 
    #    exclude=False)
    #performedPeriod: Optional[Period] = Field(
    #    None, 
    #    exclude=False)
    #performedString: Optional[str] = Field(
    #    None, 
    #    exclude=False)
    #performedAge: Optional[int] = Field(
    #    None, 
    #    exclude=False)
    #performedRange: Optional[Range] = Field(
    #    None, 
    #    exclude=False)
    performed: Optional[Union[dateTime, Period, str, int]] = Field(
        None,
        title="When the procedure was performed")
    recorder: Optional[Reference] = Field(
        None,
        enum_reference_types=["Patient","RelatedPerson","Practitioner","PractitionerRole"],
        title="Who recorded the procedure")
    asserter: Optional[Practitioner] = Field(
        None,
        enum_reference_types=["Patient","RelatedPerson","Practitioner","PractitionerRole"],
        title="Person who asserts this procedure")
    performer: Optional[Sequence[ProcedurePerformer]] = Field(
        None,
        title="The people who performed the procedure")
    location: Optional[Reference] = Field(
        None,
        enum_reference_types=["Location"],
        title="Where the procedure happened")
    reasonCode: Optional[List[CodeableConcept]] = Field(
        None,
        title="Coded reason procedure performed")
    reasonReference: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["Condition","Observation","DiagnosticReport","DocumentReference"],
        title="The justification that the procedure was performed")
    bodySite: Optional[List[CodeableConcept]] = Field(
        None,
        title="Target body sites")
    complication: Optional[List[CodeableConcept]] = Field(
        None,
        title="Complication following the procedure")
    complicationDetail: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["Condition"])
    followUp: Optional[List[CodeableConcept]] = Field(
        None,
        title="Instructions for follow up")
    note: Optional[List[Annotation]] = Field(
        None,
        title="Additional information about the procedure")
    focalDevice: Optional[List[ProcedureFocalDevice]] = Field(
        None,
        title="Device that was changed")
    usedReference: Optional[List[Reference]] = Field(
        None,
        enum_reference_types=["Device","Medication","Substance"],
        title="Items used during procedure")
    usedCode: Optional[List[CodeableConcept]] = Field(
        None,
        title="Coded items used during the procedure")