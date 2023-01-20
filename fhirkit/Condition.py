try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type:ignore
from typing import Optional, Union, List, Sequence
from pydantic import Field, validator
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
)
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Practitioner import Practitioner
from fhirkit.Organization import Organization



from fhirkit.Resource import DomainResource, ResourceWithMultiIdentifier
from fhirkit.elements.elements import Identifier

class ConditionStage(BackboneElement):
    summary: Optional[CodeableConcept] = Field(None)
    assessment: Optional[Sequence[Reference]] = Field(None)
    type: Optional[CodeableConcept] = Field(None)

class ConditionEvidence(BackboneElement):
    code: Optional[Sequence[CodeableConcept]] = Field(None)
    detail: Optional[Sequence[Reference]] = Field(None)

class Condition(DomainResource, ResourceWithMultiIdentifier):
    resourceType: Literal["Condition"] = Field("Condition", const=True)
    identifier: Sequence[Identifier] = Field([])
    clinicalStatus: Optional[CodeableConcept] = Field(None)
    verificationStatus: Optional[CodeableConcept] = Field(None)
    category: Optional[Sequence[CodeableConcept]] = Field(None)
    severity: Optional[CodeableConcept] = Field(None)
    code: Optional[CodeableConcept] = Field(None)
    bodySite: Optional[Sequence[CodeableConcept]] = Field(None)
    subject: Optional[Reference] = Field(None)
    encounter: Optional[Reference] = Field(None)
    onsetDateTime: Optional[dateTime] = Field(None)
    onsetAge: Optional[Age] = Field(None)
    onsetPeriod: Optional[Period] = Field(None)
    onsetRange: Optional[Range] = Field(None)
    onsetString: Optional[str] = Field(None)
    onset: Optional[Union[dateTime, Age, Period, Range, str]] = ChoiceType(None)
    abatementDateTime: Optional[dateTime] = Field(None)
    abatementAge: Optional[Age] = Field(None)
    abatementBoolean: Optional[bool] = Field(None)
    abatementPeriod: Optional[Period] = Field(None)
    abatementRange: Optional[Range] = Field(None)
    abatementString: Optional[str] = Field(None)
    abatement: Optional[Union[dateTime, Age, bool, Period, Range, str]] = ChoiceType(None)
    recordedDate: Optional[dateTime] = Field(None)
    recorder: Optional[Reference] = Field(None)
    asserter: Optional[Reference] = Field(None)
    stage: Optional[Sequence[ConditionStage]] = Field(None)
    evidence: Optional[Sequence[ConditionEvidence]] = Field(None)

