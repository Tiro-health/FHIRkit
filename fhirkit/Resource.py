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
)
from fhirkit.metadata_types import ContactDetail


class Meta(BaseModel):
    versionId: Optional[Id]
    lastUpdated: Optional[Instant]
    source: Optional[URI]
    profile: List[URI] = []
    security: List[Coding] = []
    tag: List[Coding] = []
    # Custom fields
    title: Optional[str] = Field(None, repr=False)
    pathway: Optional[str] = Field(None, repr=False)


InclusionExclusion = Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]]
AbstractSetIntStr = AbstractSet[Union[int, str]]
MappingIntStrAny = Mapping[Union[int, str], Any]

RESOURCE_MODELS = []


class Resource(BaseModel):

    _fhir_server: Optional[AbstractFHIRServer] = PrivateAttr(None)

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

    def record(
        self,
        by_alias: bool = False,
        include: InclusionExclusion = None,
        exclude: InclusionExclusion = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_empty: bool = True,
    ):
        tuple_generator = self._iter(
            False,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            exclude_empty,
        )
        return dict(self._assemble_key_recursively(tuple_generator))

    def dict(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_empty: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        """
        if skip_defaults is not None:
            warnings.warn(
                f'{self.__class__.__name__}.dict(): "skip_defaults" is deprecated and replaced by "exclude_unset"',
                DeprecationWarning,
            )
            exclude_unset = skip_defaults
        return dict(
            super()._iter(
                True,
                by_alias,
                include,
                exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_empty=exclude_empty,
                exclude_none=exclude_none,
            )
        )

    def _assemble_key_recursively(
        self,
        obj,
    ) -> Generator[Tuple[Tuple[str, ...], Element], None, None]:
        if isinstance(obj, (tuple, list)):
            for key_int, value in enumerate(obj):
                for childKeys, childValue in self._assemble_key_recursively(value):
                    yield (str(key_int), *childKeys), childValue
        elif isinstance(obj, (BackboneElement, Resource, Generator, Period, Range)):
            for key, value in obj:
                for childKeys, childValue in self._assemble_key_recursively(value):
                    yield (key, *childKeys), childValue
        else:
            yield (), obj

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
    identifier: Sequence[Identifier] = []
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
