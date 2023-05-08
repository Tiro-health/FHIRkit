from __future__ import annotations
import warnings

from fhirkit.elements.elements import Reference

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
from typing import (
    AbstractSet,
    Any,
    List,
    Dict,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    Generator,
)
from pydantic import Extra, Field, PrivateAttr
from fhirkit.BaseModel import BaseModel
from fhirkit.primitive_datatypes import URI, Code, Id, Instant, dateTime, date
from fhirkit.elements import (
    AbstractFHIRServer,
    BackboneElement,
    CodeableConcept,
    Element,
    Identifier,
    Narrative,
    Extension,
    Coding,
    Period,
    Range,
    UsageContext,
    Meta
)
from fhirkit.metadata_types import ContactDetail

InclusionExclusion = Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]]
AbstractSetIntStr = AbstractSet[Union[int, str]]
MappingIntStrAny = Mapping[Union[int, str], Any]

RESOURCE_MODELS = []

class Resource(BaseModel):

    resourceType: str
    id: Optional[str] = Field(None, repr=False)
    meta: Optional[Meta] = Field(None, repr=False)
    implicitRules: Optional[URI] = Field(None, repr=False)
    language: Optional[Code] = Field(None, repr=False)

    def __init_subclass__(cls) -> None:
        RESOURCE_MODELS.append(cls)

    def __str__(self) -> str:
        text = self.resourceType
        if self.id:
            text += f"/{self.id}"
        return text

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    def get_references(self):
        for k, v in self._iter():
            if isinstance(v, Reference):
                yield k, v

    def to_reference(self):
        return Reference(type=self.resourceType, reference=f"{self.resourceType}/{self.id}")


class DomainResource(Resource):
    text: Optional[Narrative] = Field(None, repr=False)
    contained: Sequence[Resource] = Field([], repr=False)
    extension: Sequence[Extension] = Field([], repr=False)
    modifierExtension: Sequence[Extension] = Field([], repr=False)

    def _repr_html_(self):
        if self.text:
            return self.text.div
        else:
            return repr(self)


class ResourceWithMultiIdentifier(Resource):
    identifier: Sequence[Identifier] = []


class CanonicalResource(DomainResource, ResourceWithMultiIdentifier):
    url: Optional[URI] = None
    version: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    status: Literal["draft", "active", "retired", "unknown"]
    experimental: Optional[bool] = None
    date: Optional[Union[date, dateTime]] = None
    publisher: Optional[str] = None
    contact: Sequence[ContactDetail] = []
    description: Optional[str] = None
    useContext: Sequence[UsageContext] = []
    jurisdiction: Sequence[CodeableConcept] = []
    purpose: Optional[str] = None
    copyright: Optional[str] = None