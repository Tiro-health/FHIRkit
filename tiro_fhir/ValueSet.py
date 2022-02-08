from typing import Iterable, Iterator, List, Literal, Optional
from pydantic import BaseModel, Field, HttpUrl
from tiro_fhir.CodeSystem import Coding, AbstractCoding
from tiro_fhir.Resource import Resource

class VSDesignation(BaseModel):
    language: Optional[str]
    use: Coding
    value: str

class VSConcept(BaseModel):
    code: str
    display: Optional[str]
    designation: List[VSDesignation] = Field(default=[])

class VSFilter(BaseModel):
    property: str
    op: Literal["=", "is-a","descendent-of","is-not-a","regex","in","not-in","generalizes","child-of","descendent-leaf","exists"]
    value: str

class VSInclude(BaseModel):
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
    url: Optional[HttpUrl]
    compose: VSCompose
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

    def __contains__(self, item:AbstractCoding) -> bool:
        return any(c == item for c in self)

    @property
    def has_expanded(self):
        return self.expansion is not None

    def expand(self):
        raise NotImplementedError()

    def append(self, coding:VSCodingWithDesignation):
        self.compose.include.append(
            VSInclude(system=coding.system, concept=[coding])
        )

        if self.expansion:
            self.expansion.contains.append(coding)
