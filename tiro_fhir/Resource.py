from typing import List, Optional, Sequence
from pydantic import AnyUrl, BaseModel, HttpUrl, Field
from tiro_fhir.Server import AbstractFHIRServer
from tiro_fhir.data_types import Code, Id, Instant
from tiro_fhir.elements import Narrative, Extension, Coding


class Meta(BaseModel):
    versionId: Optional[Id]
    lastUpdated: Optional[Instant]
    source: Optional[AnyUrl]
    profile: List[AnyUrl] = []
    security: List[Coding] = []
    tag: List[Coding] = []


class Resource(BaseModel):
    fhir_server: Optional[AbstractFHIRServer] = Field(None, exclude=True, repr=False)

    resourceType: str
    id: Optional[str] = Field(None, repr=False)
    meta: Optional[Meta] = Field(None, repr=False)
    implicitRules: Optional[HttpUrl] = Field(None, repr=False)
    language: Optional[Code] = Field(None, repr=False)

    class Config:
        arbitrary_types_allowed = True

    def _iter_to_element_or_datatype():
        pass

    def record(self, keys: Optional[Sequence[str]] = None):
        record = {}
        for field_name, value in self:
            if value:
                if field_name.startswith("value"):
                    field_name = "value"
                if keys and field_name not in keys:
                    continue
                record.update({field_name: value})
        return record


class DomainResource(Resource):
    text: Optional[Narrative] = Field(None, repr=False)
    contained: Sequence[Resource] = Field([], repr=False)
    extension: Sequence[Extension] = Field([], repr=False)
    modifierExtension: Sequence[Extension] = Field([], repr=False)
