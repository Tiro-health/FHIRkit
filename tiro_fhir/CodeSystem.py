from __future__ import annotations
import itertools
import logging
from time import time
from typing import List, Optional
from pydantic import BaseModel, Field

class AbstractCoding(BaseModel):
    """FHIR Terminology based model for concepts"""

    display: Optional[str]
    code: str
    system: str

    class Config:
        allow_mutation = False

class Coding(AbstractCoding):

    def __str__(self) -> str:
        return f"{self.system}|{self.code} \"{self.display}\""

    def __eq__(self, other: AbstractCoding) -> bool:
        return self.system == other.system and self.code == other.code

    def __hash__(self):
        return hash((self.system, self.code))


class CodeableConcept(BaseModel):
    """FHIR Terminology based mdoel for CodeableConcepts"""

    text: str
    coding: List[Coding] = Field(default=[])

    def __eq__(self, other: CodeableConcept) -> bool:
        return any(c1 == c2 for c1, c2 in itertools.product(self.coding, other.coding)) 


class CodeSystem(BaseModel):
    pass
