from __future__ import annotations
from ctypes import Union
from datetime import datetime
import itertools
from typing import Any, ForwardRef, Literal, Optional, Sequence
from pydantic import AnyUrl, BaseModel, Field
from tiro_fhir.data_types import Code, XHTML

class Element(BaseModel):
    id: Optional[str]
    extension: Sequence[Extension] = []

class Narrative(BaseModel):
    status: Literal["generated", "extensions", "additional", "required"]
    div: XHTML

class Extension(Element):
    url: AnyUrl
    value: Optional[Any]

Element.update_forward_refs()


class AbstractCoding(Element):
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


CodeableConcept = ForwardRef("CodeableConcept")
class CodeableConcept(BaseModel):
    """FHIR Terminology based mdoel for CodeableConcepts"""

    text: str
    coding: Sequence[Coding] = Field(default=[])

    def __eq__(self, other: Union[CodeableConcept, Coding]) -> bool:

        if isinstance(other, Coding):
            result = any(other == c for c in self.coding)
            return result
        elif isinstance(other, CodeableConcept):
            return any(
                c1 == c2 for c1, c2 in itertools.product(self.coding, other.coding)
            )
        else:
            return False

CodeableConcept.update_forward_refs()

class Period(Element):
    start: Optional[datetime]
    end: Optional[datetime]

class Reference(Element):
    reference: Optional[str]
    type: Optional[AnyUrl]
    identifier: Optional[Identifier]
    display: Optional[str]

class Identifier(Element):
    use: Optional[Code]
    type: Optional[CodeableConcept]
    system: Optional[AnyUrl]
    value: Optional[str]
    period: Optional[Period]
    assigner: Optional[Reference]

Identifier.update_forward_refs()
Reference.update_forward_refs()


class Quantity(BaseModel):
    value: float
    comparator: Optional[Literal["<", "<=", ">=", ">"]]
    unit: str
    system: AnyUrl
    code: Code

    def __str__(self) -> str:
        return f"{self.value} {self.unit}" 
