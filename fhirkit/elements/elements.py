from __future__ import annotations
import itertools
from typing import Any, ForwardRef, Optional, Sequence, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from pydantic import AnyUrl, Field
from fhirkit import BaseModel
from fhirkit.primitive_datatypes import URI, Code, XHTML, dateTime
from fhirkit.Server import AbstractFHIRServer


class Element(BaseModel):
    id: Optional[str]
    extension: Sequence[Extension] = Field([], repr=False)


class Attachment(Element):
    contentType: Optional[Code]
    language: Optional[Code]
    # TODO how to type base64 encode bytes


class Narrative(Element):
    status: Literal["generated", "extensions", "additional", "required"]
    div: XHTML


class Extension(Element):
    url: URI
    value: Optional[Any]


class BackboneElement(Element):
    modifierExtension: Sequence[Extension] = Field([], repr=False)


Narrative.update_forward_refs()
BackboneElement.update_forward_refs()
Element.update_forward_refs()


class AbstractCoding(Element):
    """FHIR Terminology based model for concepts"""

    display: Optional[str]
    code: str
    system: Optional[URI]
    version: Optional[str]

    class Config:
        allow_mutation = False


class Coding(AbstractCoding):
    def __repr__(self) -> str:
        if self.display:
            return f'"{self.display}" {self.system}|{self.code}'
        else:
            return f"{self.system}|{self.code}"

    def __str__(self) -> str:
        return self.display or f"{self.system}|{self.code}"

    def fsh(self, include_display: bool = False, include_version: bool = True):
        token = self.system
        if self.version is not None and include_version:
            token += "|" + self.version
        token += "#" + self.code
        if self.display is not None and include_display:
            token += ' "{self.display}"'
        return token

    def __eq__(self, other: AbstractCoding) -> bool:
        if isinstance(other, AbstractCoding):
            return self.system == other.system and self.code == other.code
        return False

    def __hash__(self):
        return hash((self.system, self.code))


CodeableConcept = ForwardRef("CodeableConcept")


class CodeableConcept(BaseModel):
    """FHIR Terminology based model for CodeableConcepts"""

    text: Optional[str] = None
    coding: Sequence[Coding] = Field([])
    active: Optional[bool] = None

    def __str__(self) -> str:
        return self.text

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
    start: Optional[dateTime]
    end: Optional[dateTime]


class Reference(Element):
    reference: Optional[str]
    type: Optional[URI]
    identifier: Optional[Identifier]
    display: Optional[str]

    def __repr__(self) -> str:
        if self.display is not None:
            return self.display
        if self.type is not None and self.reference is not None:
            return self.type + "/" + self.reference
        return super().__repr__()

    def resolve(self, store: AbstractFHIRServer):
        if self.reference:
            return store[self.reference.replace("urn:uuid:", "")]


class Identifier(Element):
    use: Optional[Code]
    type: Optional[CodeableConcept]
    system: Optional[URI]
    value: Optional[str]
    period: Optional[Period]
    assigner: Optional[Reference]


Identifier.update_forward_refs()
Reference.update_forward_refs()


class Quantity(Element):
    value: float
    comparator: Optional[Literal["<", "<=", ">=", ">"]]
    unit: str
    system: Optional[AnyUrl]
    code: Optional[Code]

    def __str__(self) -> str:
        return f"{self.value} {self.unit}"

    def unit_as_coding(self):
        return Coding(display=self.unit, code=self.code, system=self.system)

    def __repr__(self) -> str:
        rep = f"{self.value} {self.unit}"
        if self.comparator:
            return self.comparator + " " + rep
        return rep


class SimpleQuantity(Quantity):
    comparator: None = Field(..., const=True)


# TODO specify these derived quantities further
class Age(Quantity):
    pass


class Duration(Quantity):
    pass


class Range(Element):
    low: Optional[SimpleQuantity]
    high: Optional[SimpleQuantity]


class Ratio(Element):
    numerator: Optional[Quantity] = None
    denominator: Optional[Quantity] = None


class ContactPoint(Element):
    system: Optional[
        Literal["phone", "fax", "email", "pager", "url", "sms", "other"]
    ] = None
    value: Optional[str] = None
    use: Optional[Literal["home", "work", "temp", "old", "mobile"]] = None
    period: Optional[Period] = None


class ContactDetail(Element):
    name: Optional[str]
    telecom: Sequence[ContactPoint] = []
