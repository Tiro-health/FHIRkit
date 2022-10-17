from __future__ import annotations
from functools import total_ordering
import itertools
from typing import TYPE_CHECKING, Any, Optional, Sequence, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

from pydantic import AnyUrl, Field, ConstrainedList

if TYPE_CHECKING:
    from fhirkit.Resource import Resource
from fhirkit.BaseModel import BaseModel
from fhirkit.primitive_datatypes import URI, Code, XHTML, Instant, dateTime
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


@total_ordering
class Coding(AbstractCoding):
    system: URI

    def __repr__(self) -> str:
        if self.display:
            return f'"{self.display}" {self.system}|{self.code}'
        else:
            return f"{self.system}|{self.code}"

    def __str__(self) -> str:
        return self.display or f"{self.system}|{self.code}"

    def fsh(self, include_display: bool = False, include_version: bool = True):
        token: str = self.system
        if self.version is not None and include_version:
            token += "|" + self.version
        token += "#" + self.code
        if self.display is not None and include_display:
            token += ' "{self.display}"'
        return token

    def __eq__(self, other: object) -> bool:
        if isinstance(other, AbstractCoding):
            return self.system == other.system and self.code == other.code
        return False

    def __lt__(self, other: AbstractCoding) -> bool:
        return (self.system, self.code) < (other.system, other.code)

    def __hash__(self):
        return hash((self.system, self.code))


class CodeableConcept(BaseModel):
    """FHIR Terminology based model for CodeableConcepts"""

    text: Optional[str] = None
    coding: Sequence[Coding] = Field([])
    active: Optional[bool] = None

    def __str__(self) -> str:
        return self.text or super().__str__()

    def __eq__(self, other: object) -> bool:

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

    def resolve(self, store: AbstractFHIRServer) -> Union["Resource", None]:
        if self.reference:
            return store[self.reference.replace("urn:uuid:", "")]
        return None


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


AdministrativeGender = Literal["male", "female", "other", "unknown"]


HumanNameUse = Literal[
    "usual",
    "official",
    "temp",
    "nickname",
    "anonymous",
    "old",
    "maiden",
]


class HumanName(Element):
    use: Optional[HumanNameUse] = Field(None, repr=True)
    text: Optional[str] = Field(None, repr=True)
    family: Optional[str] = Field(None, repr=True)
    given: Sequence[str] = Field([], repr=True)
    prefix: Sequence[str] = Field([], repr=True)
    suffix: Sequence[str] = Field([], repr=True)
    period: Optional[Period] = Field(None, repr=True)


AddressUse = Literal[
    "home",
    "work",
    "temp",
    "old",
    "billing - purpose of this address",
]

AddressType = Literal["postal", "physical", "both"]


class Address(Element):
    use: AddressUse = Field("home", repr=True)
    type: AddressType = Field("postal", repr=True)
    text: Optional[str] = Field(None, repr=True)
    line: Sequence[str] = Field([], repr=True)
    city: Optional[str] = Field(None, repr=True)
    district: Optional[str] = Field(None, repr=True)
    state: Optional[str] = Field(None, repr=True)
    postalCode: Optional[str] = Field(None, repr=True)
    country: Optional[str] = Field(None, repr=True)
    period: Optional[Period] = Field(None, exclude=True)


class Annotation(Element):
    author: Optional[Reference] = Field(None, exclude=True)
    time: Optional[dateTime] = Field(None, exclude=True)
    text: str = Field(...)

class SignatureType(ConstrainedList):
    item_type = Coding
    min_items = 1
    unique_items = True
    __args__ = (Coding,)


class Signature(Element):
    type: SignatureType
    when: Instant
    who: Reference
    onBehalfOf: Optional[Reference] = None
    targetFormat: Optional[Code] = None
    sigFormat: Optional[Code] = None
    data: Optional[bytes]
