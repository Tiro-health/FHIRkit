from __future__ import annotations
from typing import (
    AbstractSet,
    Any,
    List,
    Dict,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    Generator,
)
from pydantic import AnyUrl, BaseModel, HttpUrl, Field, PrivateAttr
from fhirkit.Server import AbstractFHIRTerminologyServer
from fhirkit.data_types import Code, Id, Instant
from fhirkit.elements import BackboneElement, Element, Narrative, Extension, Coding
from fhirkit.ChoiceTypeMixin import AbstractChoiceTypeMixin


class Meta(BaseModel):
    versionId: Optional[Id]
    lastUpdated: Optional[Instant]
    source: Optional[AnyUrl]
    profile: List[AnyUrl] = []
    security: List[Coding] = []
    tag: List[Coding] = []


class Resource(AbstractChoiceTypeMixin, BaseModel):
    _fhir_server: Optional[AbstractFHIRTerminologyServer] = PrivateAttr(None)

    resourceType: str
    id: Optional[str] = Field(None, repr=False)
    meta: Optional[Meta] = Field(None, repr=False)
    implicitRules: Optional[HttpUrl] = Field(None, repr=False)
    language: Optional[Code] = Field(None, repr=False)

    def record(
        self,
        by_alias: bool = False,
        include: Union[
            AbstractSet[Union[int, str]], Mapping[Union[int, str], any]
        ] = None,
        exclude: Union[
            AbstractSet[Union[int, str]], Mapping[Union[int, str], any]
        ] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        exclude_choice_type: bool = True,
        exclude_polymorphic: bool = False,
    ):
        tuple_generator = self._iter(
            False,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            exclude_none,
            exclude_choice_type=exclude_choice_type,
            exclude_polymorphic=exclude_polymorphic,
        )
        return dict(self._assemble_key_recursively(tuple_generator))

    def dict(
        self,
        *,
        by_alias: bool = False,
        include: Union[
            AbstractSet[Union[int, str]], Mapping[Union[int, str], any]
        ] = None,
        exclude: Union[
            AbstractSet[Union[int, str]], Mapping[Union[int, str], any]
        ] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return dict(
            super()._iter(
                True,
                by_alias,
                include,
                exclude,
                exclude_unset,
                exclude_defaults,
                exclude_none,
                exclude_choice_type=False,
            )
        )

    def _assemble_key_recursively(
        self, obj: Union[Element, Resource]
    ) -> Generator[Tuple[Tuple[str, ...], Element]]:
        if isinstance(obj, (tuple, list)):
            for key, value in enumerate(obj):
                for childKeys, childValue in self._assemble_key_recursively(value):
                    yield (key, *childKeys), childValue
        elif isinstance(obj, (BackboneElement, Resource, Generator)):
            for key, value in obj:
                for childKeys, childValue in self._assemble_key_recursively(value):
                    yield (key, *childKeys), childValue
        else:
            yield (), obj

    @property
    def choice_type_fields(self) -> Set[str]:
        return set()

    @property
    def polymorphic_fields(self) -> Set[str]:
        return set()

    class Config:
        arbitrary_types_allowed = True


class DomainResource(Resource):
    text: Optional[Narrative] = Field(None, repr=False)
    contained: Sequence[Resource] = Field([], repr=False)
    extension: Sequence[Extension] = Field([], repr=False)
    modifierExtension: Sequence[Extension] = Field([], repr=False)
