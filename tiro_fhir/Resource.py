from typing import Any, Optional
from pydantic import BaseModel
from tiro_fhir.Server import AbstractFHIRServer


class Resource(BaseModel):
    fhir_server: Optional[AbstractFHIRServer]
    class Config:
        arbitrary_types_allowed = True
