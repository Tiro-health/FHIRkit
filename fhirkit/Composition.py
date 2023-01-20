
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
    Annotation,
    BackboneElement,
)
from fhirkit.primitive_datatypes import dateTime
from fhirkit.Practitioner import Practitioner
from fhirkit.Organization import Organization

class CompositionEventType(BackboneElement):
    code: Optional[CodeableConcept] = Field(None, repr=True)
    period: Optional[Period] = Field(None, repr=True)
    detail: Optional[List[Reference]] = Field([], repr=True)

class CompositionRelatesTo(BackboneElement):
    code: Optional[CodeableConcept] = Field(None, repr=True)
    targetIdentifier: Optional[Identifier] = Field(None, repr=True)
    targetReference: Optional[Reference] = Field(None, repr=True)
    target: Optional[Union[Identifier, Reference]] = ChoiceType(None)
    
class CompositionSection(BackboneElement):
    title: str = Field(None, repr=True)
    code: Optional[CodeableConcept] = Field(None, repr=True)
    text: Optional[Annotation] = Field(None, repr=True)
    mode: Optional[CodeableConcept] = Field(None, repr=True)
    orderedBy: Optional[CodeableConcept] = Field(None, repr=True)
    entry: Optional[List[Reference]] = Field([], repr=True)
    emptyReason: Optional[CodeableConcept] = Field(None, repr=True)
    #section: Optional[List[CompositionSection]] = Field([], repr=True)

CompositionStatus = Literal["preliminary", "final", "amended", "entered-in-error"]

class Composition(DomainResource, ResourceWithMultiIdentifier):

    resourceType: Literal["Composition"] = Field("Composition", const=True)
    author: Optional[Reference] = Field(None, repr=True)
    category: Optional[CodeableConcept] = Field(None, repr=True)
    custodian: Optional[Reference] = Field(None, repr=True)
    date: Optional[dateTime] = Field(None, exclude=True)
    encounter: Optional[Reference] = Field(None, repr=True)
    event: Optional[Sequence[CompositionEventType]] = Field([], repr=True)
    identifier: Optional[Sequence[Identifier]] = Field([], repr=True)
    relatesTo: Optional[Sequence[CompositionRelatesTo]] = Field([], repr=True)
    section: Optional[Sequence[CompositionSection]] = Field([], repr=True)
    status: CompositionStatus = Field("final", repr=True)
    subject: Optional[Reference] = Field(None, repr=True)
    title: str = Field(None, repr=True)
    type: Optional[CodeableConcept] = Field(None, repr=True)

