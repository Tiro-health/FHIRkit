from __future__ import annotations
from datetime import datetime
import itertools
from typing import Any, ClassVar, ForwardRef, Optional, Sequence, Set, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from pydantic import AnyUrl, BaseModel, Field, HttpUrl, validator
from fhirkit.data_types import URI, Code, XHTML
from fhirkit.ChoiceTypeMixin import validate_choice_types, ChoiceTypeMixinBase


class Element(BaseModel):
    id: Optional[str]
    extension: Sequence[Extension] = Field([], repr=False)


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
    system: Optional[Union[HttpUrl, str]]
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
    coding: Sequence[Coding] = Field(default=[])
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
    start: Optional[datetime]
    end: Optional[datetime]


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


class UsageContext(Element, ChoiceTypeMixinBase):
    code: Coding
    choice_type_fields: ClassVar[Set[str]] = {
        "valueQuantity",
        "valueRange",
        "valueCodeableConcept",
        "valueReference",
    }
    polymorphic_fields: ClassVar[Set[str]] = {"value"}
    valueQuantity: Optional[Quantity] = None
    valueRange: Optional[Range] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueReference: Optional[Reference] = None
    value: Union[Quantity, Range, CodeableConcept, Reference] = None

    @validator("value", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, value, values):
        return validate_choice_types(
            cls,
            value,
            values,
            {"valueQuantity", "valueRange", "valueCodeableConcept", "valueReference"},
            "value",
        )
