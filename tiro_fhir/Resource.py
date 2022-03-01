from __future__ import annotations
from typing import List, Optional, Sequence, Tuple, Union, Generator
from pydantic import AnyUrl, BaseModel, HttpUrl, Field, PrivateAttr
from tiro_fhir.Server import AbstractFHIRServer
from tiro_fhir.data_types import Code, Id, Instant
from tiro_fhir.elements import BackboneElement, Element, Narrative, Extension, Coding


class Meta(BaseModel):
    versionId: Optional[Id]
    lastUpdated: Optional[Instant]
    source: Optional[AnyUrl]
    profile: List[AnyUrl] = []
    security: List[Coding] = []
    tag: List[Coding] = []


class Resource(BaseModel):
    _fhir_server: Optional[AbstractFHIRServer] = PrivateAttr(None)

    resourceType: str
    id: Optional[str] = Field(None, repr=False)
    meta: Optional[Meta] = Field(None, repr=False)
    implicitRules: Optional[HttpUrl] = Field(None, repr=False)
    language: Optional[Code] = Field(None, repr=False)

    def to_record(self, keys: Optional[Sequence[str]]):
        return dict(
            filter(
                lambda t: t[1] is not None,
                self._assemble_key_recursively(self),
            ),
        )

    def _assemble_key_recursively(
        self, obj: Union[Element, Resource]
    ) -> Generator[Tuple[Tuple[str, ...], Element]]:
        if isinstance(obj, (tuple, list)):
            for key, value in enumerate(obj):
                for childKeys, childValue in self._assemble_key_recursively(value):
                    yield (key, *childKeys), childValue
        elif isinstance(obj, (BackboneElement, Resource)):
            for key, value in obj:
                for childKeys, childValue in self._assemble_key_recursively(value):
                    yield (key, *childKeys), childValue
        else:
            yield (), obj

    class Config:
        arbitrary_types_allowed = True


class DomainResource(Resource):
    text: Optional[Narrative] = Field(None, repr=False)
    contained: Sequence[Resource] = Field([], repr=False)
    extension: Sequence[Extension] = Field([], repr=False)
    modifierExtension: Sequence[Extension] = Field([], repr=False)
