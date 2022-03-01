from typing import Iterable, Iterator, List, Literal, Optional, Union
from pydantic import AnyUrl, BaseModel, Field, HttpUrl
from tiro_fhir.elements import BackboneElement, CodeableConcept, Coding, AbstractCoding
from tiro_fhir.Resource import Resource


class VSDesignation(BaseModel):
    language: Optional[str]
    use: Coding
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
    system: HttpUrl
    version: Optional[str]
    concept: Iterable[VSConcept] = Field(default=[])
    filter: Iterable[VSFilter] = Field(default=[])
    valueSet: Iterable[HttpUrl] = Field(default=[])


class VSCompose(BaseModel):
    include: List[VSInclude]


class VSCodingWithDesignation(Coding):
    designation: List[VSDesignation] = Field(default=[])


class VSExpansion(BaseModel):
    total: Optional[int]
    contains: List[VSCodingWithDesignation]


class ValueSet(Resource):
    resourceType = Field("ValueSet", const=True)
    url: Optional[AnyUrl]
    name: Optional[str]
    compose: Optional[VSCompose]
    expansion: Optional[VSExpansion]

    def __iter__(self) -> Iterator[Coding]:
        if not self.has_expanded:
            self.expand()
        for coding in self.expansion.contains:
            yield coding

    def __len__(self) -> Iterator[Coding]:
        if not self.has_expanded:
            self.expand()
        return self.expansion.total or len(self.expansion.contains)

    def __contains__(self, item: Union[AbstractCoding, CodeableConcept]) -> bool:
        if isinstance(item, CodeableConcept):
            return any(c in self for c in item.coding)
        elif isinstance(item, AbstractCoding):
            return any(c == item for c in self)
        else:
            return False

    @property
    def has_expanded(self):
        return self.expansion is not None

    def expand(self):
        raise NotImplementedError()

    def append(self, coding: VSCodingWithDesignation):
        self.compose.include.append(VSInclude(system=coding.system, concept=[coding]))

        if self.expansion:
            self.expansion.contains.append(coding)


class SimpleValueSet(ValueSet):
    def __init__(self, *args: VSCodingWithDesignation, **kwargs):
        assert "expansion" not in kwargs
        super().__init__(
            expansion=VSExpansion(contains=[c.dict() for c in args], total=len(args)),
            **kwargs
        )
