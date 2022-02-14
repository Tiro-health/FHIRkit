from typing import List, Optional, Sequence
from pydantic import AnyUrl, BaseModel, HttpUrl 
from tiro_fhir.Server import AbstractFHIRServer
from tiro_fhir.data_types import Code, Id, Instant
from tiro_fhir.elements import Narrative, Extension, Coding
class Meta(BaseModel):
    versionId: Optional[Id]
    lastUpdated: Optional[Instant]
    source: Optional[AnyUrl]
    profile:  List[AnyUrl] = []
    security: List[Coding] = []
    tag: List[Coding]= []
class Resource(BaseModel):
    fhir_server: Optional[AbstractFHIRServer]

    resourceType: str
    id: Optional[str]
    meta: Optional[Meta]
    implicitRules: Optional[HttpUrl]
    language: Optional[Code]
    class Config:
        arbitrary_types_allowed = True

    def record(self):
        pass
class DomainResource(Resource):
    text: Narrative
    contained: Sequence[Resource]
    extension: Sequence[Extension]
    modifierExtension: Sequence[Extension]

