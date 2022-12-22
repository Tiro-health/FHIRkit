from __future__ import annotations
from typing import (
    Any,
    ClassVar,
    Iterable,
    Optional,
    Sequence,
    Set,
    TypeVar,
    Union,
    Generator,
)

from fhirkit.choice_type import ChoiceType

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

from pydantic import Field, StrictBool, StrictStr, validator
from fhirkit.Resource import CanonicalResource
from fhirkit.choice_type import deterimine_choice_type
from fhirkit.elements import (
    BackboneElement,
    CodeableConcept,
    Coding,
    Identifier,
    UsageContext,
)
from fhirkit.primitive_datatypes import URI, Code, dateTime, date
from fhirkit.metadata_types import ContactDetail


class CodeLookupError(KeyError):
    pass


class CSConceptDesignation(BackboneElement):
    language: Optional[Code]
    use: Optional[Coding]
    value: str


class CSConceptProperty(BackboneElement):
    code: Code
    valueBoolean: Optional[StrictBool] = Field(None, exclude=True)
    valueString: Optional[StrictStr] = Field(None, exclude=True)
    valueCode: Optional[Code] = Field(None, exclude=True)
    valueCoding: Optional[Coding] = Field(None, exclude=True)
    valueDateTime: Optional[dateTime] = Field(None, exclude=True)
    valueDecimal: Optional[float] = Field(None, exclude=True)
    value: Union[StrictBool, StrictStr, Code, Coding, dateTime, float] = ChoiceType(
        None
    )

    @validator("value", pre=True, always=True, allow_reuse=True)
    def validate_value(cls, v, values, field):
        return deterimine_choice_type(cls, v, values, field)

    def __str__(self) -> str:
        return str(self.code) + ": " + str(self.value)


class CSConcept(BackboneElement):
    code: Code
    display: Optional[str]
    definition: Optional[str]
    designation: Sequence[CSConceptDesignation] = []
    property: Sequence[CSConceptProperty] = []
    concept: Sequence[CSConcept] = []

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            for param in self.property:
                if param.code == __name:
                    return param.value
            raise

    def __str__(self) -> str:
        return (
            f"#{self.code} '{self.display}'"
            + "\nproperties: \n"
            + "\n".join(" " + str(p) for p in self.property if p.value is not None)
        )


class CSConceptLookup(CSConcept):
    name: str


def traverse_concepts(
    s: Iterable[CSConcept],
) -> Generator[CSConcept, None, None]:
    for c in s:
        yield c
        if len(c.concept) > 0:
            yield from traverse_concepts(c.concept)


class CodeSystem(CanonicalResource):
    resourceType = Field("CodeSystem", const=True)
    url: Optional[URI]
    identifier: Sequence[Identifier] = []
    version: Optional[str]
    name: Optional[str]
    title: Optional[str]
    status: Literal["draft", "active", "retired", "unknown"]
    experimental: Optional[bool]
    date: Optional[Union[date, dateTime]]
    publisher: Optional[str]
    contact: Sequence[ContactDetail] = []
    description: Optional[str]
    useContext: Sequence[UsageContext] = []
    jurisdiction: Sequence[CodeableConcept] = []
    purpose: Optional[str]
    copyright: Optional[str]
    caseSensitive: Optional[bool]
    valueSet: Optional[URI]
    hierarchyMeaning: Optional[
        Literal["grouped-by", "is-a", "part-of", "classified-with"]
    ]
    compositional: Optional[bool]
    versionNeeded: Optional[bool]
    content: Literal["not-present", "example", "fragment", "complete", "supplement"]
    supplements: Optional[URI]
    count: Optional[int]
    concept: Sequence[CSConcept] = []

    def lookup(
        self,
        code: Optional[Code] = None,
        coding: Optional[Coding] = None,
        date: Optional[dateTime] = None,
        displayLanguage: Optional[Code] = None,
        property: Optional[Code] = None,
    ):
        if len(self.concept) == 0:
            raise RuntimeWarning(
                "No strategy to lookup codes or concepts if concepts are not explicitly available under 'CodeSystem.concept'"
            )

        if self.name is None:
            raise RuntimeWarning("The CodeSystem has no name to use as display name")
        assert (
            code is not None or coding is not None
        ), "At least a code or coding is needed to lookup."
        for concept in traverse_concepts(self.concept):

            if (concept.code == code) or (
                coding
                and concept.code == coding.code
                and concept.display == coding.display
            ):
                return CSConceptLookup(
                    name=self.name,
                    **concept.dict(
                        include={
                            "code",
                            "designation",
                            "property",
                            "display",
                            "version",
                        }
                    ),
                )

        raise CodeLookupError(
            f"No concept found in CodeSystem for given code/coding. (code={code}, coding={coding})"
        )

    def iter(self) -> Generator[CSConcept, None, None]:
        yield from traverse_concepts(self.concept)

    def __iter__(self):
        return self.iter()

    def __len__(self):
        if self.count:
            return self.count
        if self.content == "complete":
            self.count = len(self)
        raise ValueError(
            "CodeSystem.count is None and we have not strategy to estimate the number of concepts when CodeSystem.content != 'complete'"
        )

    def __getitem__(self, key: Code | Coding) -> CSConceptLookup:

        if isinstance(key, (Code, str)):
            return self.lookup(code=key)
        elif isinstance(key, Coding):
            return self.lookup(coding=key)
        raise KeyError("Key should be a Code or a Coding but received " + key)


CodeSystem.update_forward_refs()
for cs_subclass in CodeSystem.__subclasses__():
    cs_subclass.update_forward_refs()
CSConcept.update_forward_refs()
