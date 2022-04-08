from __future__ import annotations
from typing import Any, ClassVar, Literal, Optional, Sequence, Set, Union
from pydantic import AnyUrl, Field, StrictBool, StrictStr, validator
from tiro_fhir.Resource import DomainResource
from tiro_fhir.OperationOutcome import OperationOutcome, OperationOutcomeException
from tiro_fhir.ChoiceTypeMixin import ChoiceTypeMixinBase, validate_choice_types
from tiro_fhir.elements import (
    BackboneElement,
    CodeableConcept,
    Coding,
    Identifier,
    UsageContext,
)
from tiro_fhir.data_types import Code, dateTime
from tiro_fhir.metadata_types import ContactDetail


class CSConceptDesignation(BackboneElement):
    language: Optional[Code]
    use: Optional[Coding]
    value: str


class CSConceptPropertyValueChoiceTypeMixin(ChoiceTypeMixinBase):
    _choice_type_fields: ClassVar[Set[str]] = [
        "valueBoolean",
        "valueString",
        "valueCode",
        "valueCoding",
        "valueDateTime",
        "valueDecimal",
    ]
    _polymorphic_field: ClassVar[Set[str]] = "value"
    valueBoolean: Optional[StrictBool] = Field(None)
    valueString: Optional[StrictStr] = Field(None)
    valueCode: Optional[Code] = Field(None)
    valueCoding: Optional[Coding] = Field(None)
    valueDateTime: Optional[dateTime] = Field(None)
    valueDecimal: Optional[float] = Field(None)
    value: Union[StrictBool, StrictStr, Code, Coding, dateTime, float] = Field(
        None, exclude=True
    )

    validate_value = validator("value", pre=True, always=True, allow_reuse=True)(
        validate_choice_types
    )


class CSConceptProperty(BackboneElement, CSConceptPropertyValueChoiceTypeMixin):
    code: Code


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
            super().__str__()
            + "properties: \n"
            + "\n".join(" " + str(p) for p in self.parameter)
        )


class CSConceptLookup(CSConcept):
    name: str


class CodeSystem(DomainResource):
    resourceType = Field("CodeSystem", const=True)
    url: Optional[AnyUrl]
    identifier: Sequence[Identifier] = []
    version: Optional[str]
    name: Optional[str]
    title: Optional[str]
    status: Literal["draft", "active", "retired", "unknown"]
    experimental: Optional[bool]
    date: Optional[dateTime]
    publisher: Optional[str]
    contact: Sequence[ContactDetail] = []
    description: Optional[str]
    useContext: Sequence[UsageContext] = []
    jurisdiction: Sequence[CodeableConcept] = []
    purpose: Optional[str]
    copyright: Optional[str]
    caseSensitive: Optional[bool]
    valueSet: Optional[AnyUrl]
    hierarchyMeaning: Optional[
        Literal["grouped-by", "is-a", "part-of", "classified-with"]
    ]
    compositional: Optional[bool]
    versionNeeded: Optional[bool]
    content: Literal["not-present", "example", "fragment", "complete", "supplement"]
    supplements: Optional[AnyUrl]
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
        for concept in self.concept:

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
                        },
                        exclude_unset=True,
                    ),
                )

        raise ValueError(
            f"No concept found in CodeSystem for given code/coding. (code={code}, coding={coding})"
        )

    def __getitem__(self, key: Code | Coding) -> CSConceptLookup:
        if isinstance(key, (Code, str)):
            return self.lookup(code=key)
        elif isinstance(key, Coding):
            return self.lookup(coding=key)
        raise KeyError("Key should be a Code or a Coding but received " + key)

    CSConcept.update_forward_refs()
