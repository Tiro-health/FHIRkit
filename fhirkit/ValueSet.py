from datetime import date, datetime

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from typing import Iterable, List, Optional, Sequence, Union
from pydantic import Field
from fhirkit.BaseModel import BaseModel
from fhirkit.primitive_datatypes import URI, dateTime
from fhirkit.elements import (
    BackboneElement,
    CodeableConcept,
    Coding,
    Narrative,
    UsageContext,
)
from fhirkit.Resource import CanonicalResource


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
    system: Optional[URI] = None
    version: Optional[str] = None
    concept: Sequence[VSConcept] = Field(default=[])
    filter: Sequence[VSFilter] = Field(default=[])
    valueSet: Sequence[URI] = Field(default=[])


class VSCompose(BaseModel):
    include: List[VSInclude] = []
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
    identifier: Optional[URI] = None
    timestamp: dateTime = Field(default_factory=datetime.now)


class ValueSet(CanonicalResource):
    resourceType: Literal["ValueSet"] = Field("ValueSet", const=True)
    url: Optional[URI]
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
            assert (
                self.has_expanded
            ), "ValueSet has no expansion even after running `self.expand()`."
        return self.expansion.total or len(self.expansion.contains)

    def __contains__(self, item: Union[Coding, CodeableConcept]) -> bool:
        if not isinstance(item, (Coding, CodeableConcept)):
            return False
        return self.validate_code(item)

    @property
    def has_expanded(self):
        return self.expansion is not None

    def expand(self):
        """Override this method to implement expansion logic.
        This method should fill ValueSet.expansion.contains with concepts.

        Implementing this method enables you to iterate over the ValueSet in a for-loop.
        ```python
        class MyCustomValueSet(ValueSet)

            def expand(self):
                # some expansion logic

        vs_example = MyCustomValueSet()
        for coding in vs:
            print(coding)
        "
        """
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

        if not self.has_expanded and init_expansion_if_none:
            self.init_expansion()

        assert (
            self.expansion is not None
        ), "`self.expansion` is None after initialisation with `self.init_expansion`"
        self.expansion.contains.append(code)

    def extend(
        self,
        codes: Iterable[VSCodingWithDesignation],
        extend_compose: bool = True,
        auto_init_expansion: bool = True,
    ):
        if extend_compose:
            first_code, *_ = iter(codes)
            self.compose.include.append(
                VSInclude(system=first_code.system, concept=list(codes))
            )

        if not self.has_expanded and auto_init_expansion:
            self.init_expansion()
        assert (
            self.expansion is not None
        ), "`self.expansion` is None after initialisation with `self.init_expansion`"
        self.expansion.contains.extend(codes)


class SimpleValueSet(ValueSet):
    status: Literal["active"] = Field("active", const=True)

    def __init__(self, *args: VSCodingWithDesignation, **kwargs):
        if len(args) > 0:

            assert (
                "expansion" not in kwargs
            ), "When passing an iterable with concepts, `expansion` should be None."
            super().__init__(
                expansion=VSExpansion(
                    contains=[c.dict() for c in args], total=len(args)
                ),
                text=Narrative(
                    status="generated",
                    div="""
                <div>
                    <style scoped>
                        .dataframe tbody tr th:only-of-type {
                            vertical-align: middle;
                        }

                        .dataframe tbody tr th {
                            vertical-align: top;
                        }

                        .dataframe thead th {
                            text-align: right;
                        }
                    </style>
                    <table border="1" class="dataframe">
                        <thead>
                            <tr style="text-align: right;">
                            <th>code</th>
                            <th>display</th>
                            <th>system</th>
                            <th>version</th>
                            </tr>
                        </thead>
                        <tbody>"""
                    + "".join(
                        [
                            f"<tr><th>{c.code}</th><td>{c.display}</td><td>{c.system}</td><td>{c.version}</td></tr>"
                            for c in args
                        ]
                    )
                    + """
                        </tbody>
                    </table>
                </div>""",
                ),
                **kwargs,
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


ValueSet.update_forward_refs()
