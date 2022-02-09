from __future__ import annotations
import itertools
from typing import Union, List, Optional
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
        return f'"{self.display}" {self.system}|{self.code}'

    def __eq__(self, other: AbstractCoding) -> bool:
        if isinstance(other, AbstractCoding):
            return self.system == other.system and self.code == other.code
        return False

    def __hash__(self):
        return hash((self.system, self.code))


class CodeableConcept(BaseModel):
    """FHIR Terminology based mdoel for CodeableConcepts"""

    text: str
    coding: List[Coding] = Field(default=[])

    def __eq__(self, other: Union[CodeableConcept, Coding]) -> bool:

        # TODO handle case if other is a coding
        # Observation.code == Coding()
        if isinstance(other, Coding):
            result = any(other == c for c in self.coding)
            return result
        elif isinstance(other, CodeableConcept):
            return any(
                c1 == c2 for c1, c2 in itertools.product(self.coding, other.coding)
            )
        else:
            return False


class CodeSystem(BaseModel):
    pass
