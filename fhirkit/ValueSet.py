import abc
from datetime import date, datetime
from typing import Any, Iterable, Iterator, List, Literal, Optional, Sequence, Union
from pydantic import AnyUrl, BaseModel, Field, HttpUrl
from fhirkit.data_types import dateTime
from fhirkit.elements import BackboneElement, CodeableConcept, Coding, UsageContext
from fhirkit.Resource import Resource


class VSDesignation(BaseModel):
    language: Optional[str]
    use: Optional[Coding]
    value: str


class VSConcept(BaseModel):
    code: str
    display: Optional[str]
    designation: List[VSDesignation] = Field(default=[])


class VSFilter(BackboneElement):
    property: str
    op: Literal[
        "=",
        "is-a",
        "descendent-of",
        "is-not-a",
        "regex",
        "in",
        "not-in",
        "generalizes",
        "child-of",
        "descendent-leaf",
        "exists",
    ]
    value: str


class VSInclude(BackboneElement):
    system: Optional[HttpUrl]
    version: Optional[str]
    concept: Sequence[VSConcept] = Field(default=[])
    filter: Sequence[VSFilter] = Field(default=[])
    valueSet: Sequence[HttpUrl] = Field(default=[])


class VSCompose(BaseModel):
    include: List[VSInclude]
    exclude: List[VSInclude] = []
    property: Sequence[str] = []
    lockedDate: Optional[date]
    inactive: Optional[bool]


class VSCodingWithDesignation(Coding):
    designation: List[VSDesignation] = Field(default=[])


class VSExpansion(BaseModel):
    offset: Optional[int]
    total: Optional[int]
    contains: List[VSCodingWithDesignation] = []
    identifier: Optional[AnyUrl] = None
    timestamp: dateTime = Field(default_factory=datetime.now)


class ValueSet(Resource):
    resourceType = Field("ValueSet", const=True)
    url: Optional[AnyUrl]
    name: Optional[str]
    compose: Optional[VSCompose]
    expansion: Optional[VSExpansion]
    useContext: Sequence[UsageContext] = Field([], repr=True)

    def __iter__(self):
        if not self.has_expanded:
            self.expand()
        for coding in self.expansion.contains:
            yield coding

    def __len__(self):
        if not self.has_expanded:
            self.expand()
        return self.expansion.total or len(self.expansion.contains)

    def __contains__(self, item: Union[Coding, CodeableConcept]) -> bool:
        if not isinstance(item, (Coding, CodeableConcept)):
            return False
        return self.validate_code(item)

    @property
    def has_expanded(self):
        return self.expansion is not None

    def expand(self) -> Iterable[VSCodingWithDesignation]:
        raise NotImplementedError()

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        raise NotImplementedError()

    def init_expansion(self):
        self.expansion = VSExpansion()

    def append(
        self,
        code: VSCodingWithDesignation,
        extend_compose: bool = True,
        init_expansion_if_none: bool = True,
    ):
        if extend_compose:
            self.compose.include.append(VSInclude(system=code.system, concept=[code]))

        if self.expansion is None and init_expansion_if_none:
            self.init_expansion()

        if self.expansion:
            self.expansion.contains.append(code)

    def extend(
        self,
        codes: Iterable[VSCodingWithDesignation],
        extend_compose: bool = True,
        init_expansion_if_none: bool = True,
    ):
        if extend_compose:
            first_code, *_ = iter(codes)
            self.compose.include.append(
                VSInclude(system=first_code.system, concept=list(codes))
            )

        if self.expansion is None and init_expansion_if_none:
            self.init_expansion()

        if self.expansion:
            self.expansion.contains.extend(codes)


class SimpleValueSet(ValueSet):
    def __init__(self, *args: VSCodingWithDesignation, **kwargs):
        if len(args) > 0:

            assert (
                "expansion" not in kwargs
            ), "When passing an iterable with concepts, `expansion` should be None."
            super().__init__(
                expansion=VSExpansion(
                    contains=[c.dict() for c in args], total=len(args)
                ),
                **kwargs
            )
        else:
            super().__init__(**kwargs)

    def expand(self):
        raise UserWarning(
            "SimpleValueSet is already expanded at construction time. So it doesn't make sense to explicitly ask for expansion."
        )

    def validate_code(self, code: Union[Coding, CodeableConcept]):
        if isinstance(code, CodeableConcept):
            return any(c in self for c in code.coding)
        elif isinstance(code, Coding):
            return any(c == code for c in self)
        else:
            return False
